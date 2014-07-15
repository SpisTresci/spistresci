from django.db import models
from jsonfield import JSONField


class BookFormat(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10, blank=False)


class Bookstore(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10, blank=False)
    url = models.CharField(max_length=512L)


class BookDescription(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True)


class MasterAuthor(models.Model):
    id = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=255L, blank=True)
    first_name = models.CharField(max_length=32L, blank=True)
    middle_name = models.CharField(max_length=32L, blank=True)
    last_name = models.CharField(max_length=32L, blank=True)

    name_simplified = models.CharField(max_length=255L, blank=True)

    first_name_soundex = models.IntegerField(null=True, blank=True)
    middle_name_soundex = models.IntegerField(null=True, blank=True)
    last_name_soundex = models.IntegerField(null=True, blank=True)


class MiniAuthor(models.Model):
    id = models.IntegerField(primary_key=True)

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

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=512L, blank=True)
    cover = models.CharField(max_length=512L, blank=True)
    format = models.ManyToManyField(BookFormat)

    authors = models.ManyToManyField(MasterAuthor)


class MiniBook(models.Model):

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=512L, blank=True)
    cover = models.CharField(max_length=512L)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    format = models.ManyToManyField(BookFormat)
    master = models.ForeignKey(
        MasterBook,
        null=True,
        blank=True,
        related_name="mini_books",
    )

    authors = models.ManyToManyField(MiniAuthor)

    url = models.CharField(max_length=512L)
    bookstore = models.ForeignKey(Bookstore)
    description = models.ForeignKey(BookDescription)
    extra = JSONField()
