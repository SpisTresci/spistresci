# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from django_common.helper import md5_hash


class BloggerProfile(models.Model):

    def get_blogger_path():
        return 'bloggers/%s/' % md5_hash(max_length=16)

    user = models.OneToOneField(User)
    website = models.URLField()
    photo = models.ImageField(upload_to=get_blogger_path)
    signature = models.ImageField(upload_to=get_blogger_path)

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username

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

    author = models.ForeignKey(User, related_name="recommendations")
    masterbook = models.ForeignKey('spistresci.MasterBook')
    content = models.TextField()
    mark = models.CharField(max_length=128)
    website_path = models.CharField(max_length=512)
    promote_rate = models.IntegerField(choices=RATE_CHOICES, default=1)

    def __unicode__(self):
        return u'Recenzja %s do książki: "%s"' % (self.author.get_full_name(),
                                                  self.masterbook.title)

    class Meta:
        app_label = 'spistresci'
        db_table = 'BookRecommendation'
