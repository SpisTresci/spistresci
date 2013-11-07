from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.hashers import *
from django.utils import timezone

from spistresci.track.models import *
from spistresci.blogger.models import *

class MasterBookSolrWrapper(models.Model):
    class Meta:
        db_table="MasterBookSolrWrapper"


class BookstoreSolrWrapper(models.Model):
    class Meta:
        db_table="BookstoreSolrWrapper"


class eGazeciarzUser(models.Model):
    '''
    Reimplement AbstractBaseUser, because it cannot inherit it
    since overriding model fields is not possible in django
    at the moment.
    '''
    USERNAME_FIELD = 'username'

    id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=255L)
    username = models.CharField(max_length=150L)
    email = models.CharField(max_length=100L)
    password = models.CharField(max_length=100L)
    kindle = models.CharField(max_length=255L, blank=True)
    usertype = models.CharField(max_length=25L)
    block = models.IntegerField()
    sendemail = models.IntegerField(null=True, db_column='sendEmail', blank=True) # Field name made lowercase.
    gid = models.IntegerField()
    registerdate = models.DateTimeField(db_column='registerDate') # Field name made lowercase.

    activation = models.CharField(max_length=100L)
    params = models.TextField()

    last_login = models.DateTimeField(db_column='lastvisitDate', default=timezone.now)

    class Meta:
        db_table = 'jos_users'

    is_active = True

    REQUIRED_FIELDS = []

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_full_name(self):
        raise NotImplementedError()

    def get_short_name(self):
        raise NotImplementedError()

class MasterAuthor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255L, blank=True)
    firstname = models.CharField(max_length=32L, db_column='firstName', blank=True) # Field name made lowercase.
    middlename = models.CharField(max_length=32L, db_column='middleName', blank=True) # Field name made lowercase.
    lastname = models.CharField(max_length=32L, db_column='lastName', blank=True) # Field name made lowercase.
    name_simplified = models.CharField(max_length=255L, blank=True)
    lastname_soundex = models.IntegerField(null=True, db_column='lastName_soundex', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'MasterAuthor'

class MasterBook(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=512L, blank=True)
    cover = models.CharField(max_length=512L, blank=True)
    format_cd = models.IntegerField(null=True, blank=True)
    format_cd_mp3 = models.IntegerField(null=True, blank=True)
    format_dvd = models.IntegerField(null=True, blank=True)
    format_epub = models.IntegerField(null=True, blank=True)
    format_fb2 = models.IntegerField(null=True, blank=True)
    format_ks = models.IntegerField(null=True, blank=True)
    format_mobi = models.IntegerField(null=True, blank=True)
    format_mp3 = models.IntegerField(null=True, blank=True)
    format_pdf = models.IntegerField(null=True, blank=True)
    format_txt = models.IntegerField(null=True, blank=True)
    format_xml = models.IntegerField(null=True, blank=True)
    description = models.ForeignKey('BookDescription', null=True, blank=True)
    authors = models.ManyToManyField(MasterAuthor, through='MasterBooksMasterAuthors')
    price = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'MasterBook'

    def __unicode__(self):
        return self.title

class MasterBooksMasterAuthors(models.Model):
    book = models.ForeignKey('MasterBook', null=True, blank=True)
    author = models.ForeignKey('MasterAuthor', null=True, blank=True)
    class Meta:
        db_table = 'master_books_master_authors'

class BookDescription(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=20000L, blank=True)
    class Meta:
        db_table = 'BookDescription'
