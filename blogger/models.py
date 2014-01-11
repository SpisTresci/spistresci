# -*- coding: utf-8 -*-

from urlparse import urljoin

from django.db import models
from django.contrib.auth.models import User

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Crop, ResizeToFit

from django_common.helper import md5_hash


class BloggerProfile(models.Model):

    def get_blogger_path(instance, file_name):
        return 'bloggers/%s/%s/%s' % (instance.pk, md5_hash(max_length=16), file_name)

    user = models.OneToOneField(User)
    website = models.URLField(null=True, blank=True, verbose_name=u"Adres bloga")
    website_name = models.CharField(max_length=128, null=True, blank=True, verbose_name=u"Nazwa bloga")
    photo = models.ImageField(upload_to=get_blogger_path, null=True, blank=True, verbose_name=u"Zdjęcie")
    signature = models.ImageField(upload_to=get_blogger_path, null=True, blank=True, verbose_name=u"Podpis")
    publication_available = models.BooleanField(default=False)

    photo_thumbnail = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(150, 150),
                                                 Crop(150, 150)],
                                     format='PNG',
                                     options={'quality': 90})
    signature_thumbnail = ImageSpecField(source='signature',
                                     processors=[ResizeToFit(250, 30)],
                                     format='PNG',
                                     options={'quality': 90})

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username

    def get_recommendation_statuses(self):
        statuses = [BookRecommendation.STATUS_NEW,
                    BookRecommendation.STATUS_FOR_PUBLICATION]
        if self.publication_available:
            statuses.append(BookRecommendation.STATUS_PUBLICATED)
        choices = dict(BookRecommendation.STATUS_CHOICES)
        return map(lambda x: (x, choices[x]), statuses)

    class Meta:
        app_label = 'spistresci'
        db_table = 'BloggerProfile'


class BookRecommendation(models.Model):

    RATE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )

    STATUS_NEW = 1
    STATUS_FOR_PUBLICATION = 2
    STATUS_PUBLICATED = 3

    STATUS_CHOICES = (
        (STATUS_NEW, 'wersja robocza'),
        (STATUS_FOR_PUBLICATION, 'do publikacji'),
        (STATUS_PUBLICATED, 'opublikowana')
    )

    author = models.ForeignKey(User, related_name="recommendations")
    masterbook = models.ForeignKey('spistresci.MasterBook', verbose_name=u'Książka')

    title = models.CharField(max_length=512, verbose_name=u'Tytuł')
    content = models.TextField(verbose_name=u'Opis')
    mark = models.CharField(max_length=128, verbose_name=u'Twoja ocena (najlepiej słowna)')
    website_path = models.CharField(max_length=512, verbose_name=u'Link do recenzji na blogu')
    book_path = models.CharField(max_length=512, verbose_name=u'Link do książki')
    promote_rate = models.IntegerField(choices=RATE_CHOICES, default=1, verbose_name=u'Jak bardzo promować tę rekomendację wśród Twoich postów?',
                                       help_text=u'(1-mało, 5-bardzo)')

    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name=u'Status')
    publication_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'Recenzja %s do książki: "%s"' % (self.author.get_full_name(),
                                                  self.masterbook.title)

    class Meta:
        app_label = 'spistresci'
        db_table = 'BookRecommendation'
        ordering = ('-id',)

    def is_publicated(self):
        return self.status == self.STATUS_PUBLICATED
