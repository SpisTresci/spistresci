# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.contrib import admin
from decimal import Decimal
from django.utils import timezone
from jsonfield import JSONField


def cmp(obj1, obj2):
    if not obj1 or not obj2:
        return (0.8, False)

    return obj1.cmp(obj2)


def cmp_lists(list1, list2):
    r = ComparableMixin.Result()
    max_len = 0 if not list1 or not list2 else max(len(list1), len(list2))

    if max_len == 0:    #TODO: musza byc tutaj wprowadzone wagi, by brak wszystkich atrybutow do porownania nie powodowal mergowania
        return 0.8

    for obj1 in list1:
        for obj2 in list2:
            r.add(obj1.cmp(obj2))

    return r.matches()/float(max_len)


class ComparableMixin(object):
    accept_threshold = 1.0

    def __init__(self, *args, **kwargs):
        super(ComparableMixin, self).__init__(*args, **kwargs)

    def cmp(self, other):
        raise NotImplementedError

    def cmp_with_list(self, l_others):
        for other in l_others:
            self.cmp(other)

    class Result():
        def __init__(self):
            self.tests = []

        def add(self, (ratio, merged)):
            self.tests.append((ratio, merged))

        def addRatio(self, ratio):
            self.tests.append((ratio, False))

        def result(self):
            return self.geo_avg([r for r, m in self.tests])

        def __repr__(self):
            return str(self.result())

        def matches(self):
            return len([m for r, m in self.tests if m])

        @staticmethod
        def geo_avg(tests):
            if len(tests) == 0:
                return 0.0

            r = 1.0
            for t in tests:
                r *= t

            return r ** (1.0 / len(tests))

        @staticmethod
        def avg(tests):
            if len(tests) == 0:
                return 0.0

            return sum(tests) / float(len(tests))

    # @declared_attr
    # def declareCache(cls):
    #     cache_name = "%sCompare" % cls.__name__
    #     exec('class %s(BaseCompare, Base): pass' % cache_name)
    #     exec('cls.cache = %s' % cache_name)
    #     SqlWrapper.table_list += [cache_name]


class BookFormatType(models.Model):

    UNKNOWN = 1
    BOOK = 2
    EBOOK = 3
    AUDIOBOOK = 4

    name = models.CharField(max_length=10, blank=False)

    def __unicode__(self):
        return self.name

admin.site.register(BookFormatType)


class BookFormat(models.Model):

    name = models.CharField(max_length=10, blank=False)
    type = models.ForeignKey(BookFormatType, default=BookFormatType.UNKNOWN)

    def __unicode__(self):
        return self.name

admin.site.register(BookFormat)


class Bookstore(models.Model):

    name = models.CharField(max_length=50, blank=False)
    url = models.URLField(max_length=2048)

    def __unicode__(self):
        return self.name

admin.site.register(Bookstore)


class BookDescription(models.Model):

    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.description[:100]

admin.site.register(BookDescription)


class ISBN(ComparableMixin, models.Model):

    raw = models.CharField(max_length=50, blank=True)
    core = models.CharField(max_length=9, blank=True)
    isbn10 = models.CharField(max_length=10, blank=True)
    isbn13 = models.CharField(max_length=13, blank=True)
    valid = models.BooleanField()

    def __unicode__(self):
        return self.core

admin.site.register(ISBN)


class MasterAuthor(ComparableMixin, models.Model):

    name = models.CharField(max_length=255L, blank=True)
    first_name = models.CharField(max_length=32L, blank=True)
    middle_name = models.CharField(max_length=32L, blank=True)
    last_name = models.CharField(max_length=32L, blank=True)

    name_simplified = models.CharField(max_length=255L, blank=True)

    first_name_soundex = models.IntegerField(null=True, blank=True)
    middle_name_soundex = models.IntegerField(null=True, blank=True)
    last_name_soundex = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name

admin.site.register(MasterAuthor)


class MiniAuthor(ComparableMixin, models.Model):

    name = models.CharField(max_length=255L, blank=True)
    first_name = models.CharField(max_length=32L, blank=True)
    middle_name = models.CharField(max_length=32L, blank=True)
    last_name = models.CharField(max_length=32L, blank=True)

    name_simplified = models.CharField(max_length=255L, blank=True)

    master = models.ForeignKey(
        MasterAuthor,
        null=True,
        blank=True,
        related_name="mini_authors",
    )

    first_name_soundex = models.IntegerField(null=True, blank=True)
    middle_name_soundex = models.IntegerField(null=True, blank=True)
    last_name_soundex = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name


admin.site.register(MiniAuthor)


class BaseBook(models.Model):

    class Meta:
        abstract = True

    title = models.CharField(max_length=512L, blank=True)
    cover = models.CharField(max_length=512L, blank=True)
    formats = models.ManyToManyField(BookFormat)

    BESTSELLER__MANUALLY_SET = 1
    BESTSELLER__OF_ALL_TIME = 2
    BESTSELLER__OF_THE_DAY = 3
    BESTSELLER__OF_THE_WEEK = 4

    BESTSELLER__TYPE_CHOICES = (
        (BESTSELLER__MANUALLY_SET, u'Wybrane'),
        (BESTSELLER__OF_ALL_TIME, u'Wszechczasów'),
        (BESTSELLER__OF_THE_DAY, u'Dnia'),
        (BESTSELLER__OF_THE_WEEK, u'Tygodnia'),
    )

    bestseller_type = models.IntegerField(
        choices=BESTSELLER__TYPE_CHOICES,
        null=True,
        blank=True,
    )

    NEW__MANUALLY_SET = 1
    NEW__IN_FORMAT = 2

    NEW__TYPE_CHOICES = (
        (NEW__MANUALLY_SET, u'Wybrane'),
        (NEW__IN_FORMAT, u'W formacie'),
    )

    new_type = models.IntegerField(
        choices=NEW__TYPE_CHOICES,
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return self.title

class MasterBook(ComparableMixin, BaseBook):

    authors = models.ManyToManyField(MasterAuthor, null=True, blank=True)

    def price_lowest(self):
        return min(mini.price for mini in self.mini_books.all())

    def price_highest(self):
        return max(mini.price for mini in self.mini_books.all())

    def bookstores(self):
        bookstores = set(mini.bookstore.name for mini in self.mini_books.all())
        return list(bookstores)

admin.site.register(MasterBook)


class MiniBook(ComparableMixin, BaseBook):

    class Meta:
        unique_together = (("external_id", "bookstore"),)

    external_id = models.CharField(max_length=32)
    created_with_command = models.ForeignKey('BookstoreCommandStatus')

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    price_normal = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    url = models.URLField(max_length=2048, default='')
    pp_url = models.URLField(max_length=2048, default='')

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    bookstore = models.ForeignKey(Bookstore)
    description = models.OneToOneField(BookDescription, null=True, blank=True)
    master = models.ForeignKey(
        MasterBook,
        null=True,
        blank=True,
        related_name="mini_books",
    )

    authors = models.ManyToManyField(MiniAuthor, null=True, blank=True)
    isbns = models.ManyToManyField(ISBN, null=True, blank=True)
    extra = JSONField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
            self.created_with_command = \
                BookstoreCommandStatus.get_last_parse_command(
                    bookstore=self.bookstore
                )

        self.modified = timezone.now()
        return super(MiniBook, self).save(*args, **kwargs)

    def getCandidatesByTitle(self):

        minis = MiniBook.objects.filter(
            ~Q(bookstore=self.bookstore),
            ~Q(master=self.master),
            title__iexact=self.title,
        )

        return minis

    def getCandidatesByISBNs(self):

        minis = MiniBook.objects.filter(
            ~Q(id=self.id),
            isbns__core__in=[isbn.core for isbn in self.isbns.all()],
        )

        return minis

    def getCandidatesByAuthors(self):
        minis = MiniBook.objects.filter(
            ~Q(id=self.id),
            authors__name__in=[author.name for author in self.authors.all()]
        )

        return minis

    def updateSimilar(self, miniBook, result=None):
        low, hight = (self, miniBook) if self.id < miniBook.id else (miniBook, self)

        obj, _ = Similarity.objects.get_or_create(lower_id=low, higher_id=hight)
        if result:
            obj.result = result

        obj.save()

admin.site.register(MiniBook)


class Promotion(models.Model):
    PROMOTION_OF_THE_DAY = 1

    name = models.CharField(max_length=512L, default='')
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    banner = models.CharField(max_length=512L, null=True, blank=True)
    extra = JSONField(blank=True, null=True)

    mini_books = models.ManyToManyField(
        MiniBook,
        null=True,
        blank=True,
        related_name='promotion',
    )
    master_books = models.ManyToManyField(
        MasterBook,
        null=True,
        blank=True,
        related_name='promotion',
    )

    def __unicode__(self):
        return self.name

admin.site.register(Promotion)


class CommandStatus(models.Model):

    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    watch_dog = models.DateTimeField(auto_now_add=True)
    manual = models.BooleanField()
    partial = models.BooleanField()

    finished = models.BooleanField(default=False)
    success = models.BooleanField(default=False)

    WATCH_DOG_THRESHOLD = 60

    def feed_dog(self):
        td = timezone.timedelta(seconds=self.WATCH_DOG_THRESHOLD/4)
        if self.watch_dog + td < timezone.now():
            self.watch_dog = timezone.now()
            self.save()

    def __unicode__(self):
        return str(self.start) + ' - ' + str(self.end)


admin.site.register(CommandStatus)


class BookstoreCommandStatus(models.Model):

    cmd_status = models.ForeignKey(CommandStatus)
    bookstore = models.ForeignKey(Bookstore)

    finished = models.BooleanField(default=False)
    success = models.BooleanField(default=False)

    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    watch_dog = models.DateTimeField(auto_now_add=True)

    TYPE_FETCH = 1
    TYPE_PARSE = 2
    TYPE_ANALYZE = 3

    TYPE_CHOICES = (
        (TYPE_FETCH, u'Pobieranie'),
        (TYPE_PARSE, u'Parsowanie'),
        (TYPE_ANALYZE, u'Analiza/Łączenie'),
    )

    type = models.IntegerField(choices=TYPE_CHOICES)
    extra = JSONField()

    WATCH_DOG_THRESHOLD = 60

    def feed_dog(self):
        self.cmd_status.feed_dog()
        td = timezone.timedelta(seconds=self.WATCH_DOG_THRESHOLD/4)
        if self.watch_dog + td < timezone.now():
            self.watch_dog = timezone.now()
            self.save()

    def is_dog_fed(self):
        td = timezone.timedelta(seconds=self.WATCH_DOG_THRESHOLD)
        return self.watch_dog + td > timezone.now()

    def __unicode__(self):
        return str(self.start) + ' - ' + str(self.end)

    @staticmethod
    def get_last_parse_command(bookstore):
        return BookstoreCommandStatus.objects.filter(
            type=BookstoreCommandStatus.TYPE_PARSE,
            bookstore=bookstore,
        ).latest('id')

admin.site.register(BookstoreCommandStatus)


class Similarity(models.Model):

    lower_id = models.ForeignKey(MiniBook, related_name='low_id')
    higher_id = models.ForeignKey(MiniBook, related_name='high_id')
    result = models.FloatField(null=True, blank=True)

    def lower_masterbook(self):
        return self.lower_id.master

    def higher_masterbook(self):
        return self.higher_id.master
