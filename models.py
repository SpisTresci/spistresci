# -*- coding: utf-8 -*-
from django.db import models
from decimal import Decimal
from django.utils import timezone
from jsonfield import JSONField


class BookFormat(models.Model):

    name = models.CharField(max_length=10, blank=False)


class Bookstore(models.Model):

    name = models.CharField(max_length=50, blank=False)
    url = models.CharField(max_length=512L)


class BookDescription(models.Model):

    description = models.TextField(blank=True)


class ISBN(models.Model):

    raw = models.CharField(max_length=50, blank=True)
    core = models.CharField(max_length=9, blank=True)
    isbn10 = models.CharField(max_length=10, blank=True)
    isbn13 = models.CharField(max_length=13, blank=True)
    valid = models.BooleanField()


class MasterAuthor(models.Model):

    name = models.CharField(max_length=255L, blank=True)
    first_name = models.CharField(max_length=32L, blank=True)
    middle_name = models.CharField(max_length=32L, blank=True)
    last_name = models.CharField(max_length=32L, blank=True)

    name_simplified = models.CharField(max_length=255L, blank=True)

    first_name_soundex = models.IntegerField(null=True, blank=True)
    middle_name_soundex = models.IntegerField(null=True, blank=True)
    last_name_soundex = models.IntegerField(null=True, blank=True)


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


class MasterBook(models.Model):

    title = models.CharField(max_length=512L, blank=True)
    cover = models.CharField(max_length=512L, blank=True)
    format = models.ManyToManyField(BookFormat)

    authors = models.ManyToManyField(MasterAuthor)


class MiniBook(models.Model):

    class Meta:
        unique_together = (("external_id", "bookstore"),)

    external_id = models.IntegerField()
    title = models.CharField(max_length=512L, default='')
    cover = models.CharField(max_length=512L, default='')
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
    formats = models.ManyToManyField(BookFormat)

    extra = JSONField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(MiniBook, self).save(*args, **kwargs)


class CommandStatus(models.Model):

    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    manual = models.BooleanField()
    partial = models.BooleanField()

    finished = models.BooleanField(default=False)
    success = models.BooleanField(default=False)


class BookstoreCommandStatus(models.Model):

    cmd_status = models.ForeignKey(CommandStatus)
    bookstore = models.ForeignKey(Bookstore)

    finished = models.BooleanField(default=False)
    success = models.BooleanField(default=False)

    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)

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
