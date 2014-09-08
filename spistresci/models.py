# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from decimal import Decimal
from django.utils import timezone
from jsonfield import JSONField


class BookFormatType(models.Model):

    name = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.name

admin.site.register(BookFormatType)


class BookFormat(models.Model):

    name = models.CharField(max_length=10, blank=False)
    type = models.ForeignKey(BookFormatType)

    def __str__(self):
        return self.name

admin.site.register(BookFormat)


class Bookstore(models.Model):

    name = models.CharField(max_length=50, blank=False)
    url = models.CharField(max_length=512L)

    def __str__(self):
        return self.name

admin.site.register(Bookstore)


class BookDescription(models.Model):

    description = models.TextField(blank=True)

admin.site.register(BookDescription)


class ISBN(models.Model):

    raw = models.CharField(max_length=50, blank=True)
    core = models.CharField(max_length=9, blank=True)
    isbn10 = models.CharField(max_length=10, blank=True)
    isbn13 = models.CharField(max_length=13, blank=True)
    valid = models.BooleanField()

admin.site.register(ISBN)


class MasterAuthor(models.Model):

    name = models.CharField(max_length=255L, blank=True)
    first_name = models.CharField(max_length=32L, blank=True)
    middle_name = models.CharField(max_length=32L, blank=True)
    last_name = models.CharField(max_length=32L, blank=True)

    name_simplified = models.CharField(max_length=255L, blank=True)

    first_name_soundex = models.IntegerField(null=True, blank=True)
    middle_name_soundex = models.IntegerField(null=True, blank=True)
    last_name_soundex = models.IntegerField(null=True, blank=True)

admin.site.register(MasterAuthor)


class MiniAuthor(models.Model):

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


class MasterBook(BaseBook):

    authors = models.ManyToManyField(MasterAuthor, null=True, blank=True)

    def price_lowest(self):
        return min(mini.price for mini in self.mini_books.all())

    def price_highest(self):
        return max(mini.price for mini in self.mini_books.all())

    def bookstores(self):
        bookstores = set(mini.bookstore.name for mini in self.mini_books.all())
        return list(bookstores)

admin.site.register(MasterBook)


class MiniBook(BaseBook):

    class Meta:
        unique_together = (("external_id", "bookstore"),)

    external_id = models.IntegerField()

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

    url = models.CharField(max_length=512L, default='')
    pp_url = models.CharField(max_length=512L, default='')

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    bookstore = models.ForeignKey(Bookstore)
    description = models.ForeignKey(BookDescription, null=True, blank=True)
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
        self.modified = timezone.now()
        return super(MiniBook, self).save(*args, **kwargs)

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

admin.site.register(BookstoreCommandStatus)