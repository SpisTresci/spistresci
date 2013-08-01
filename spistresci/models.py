from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.hashers import *
from django.utils import timezone

class MasterBookSolrWrapper(models.Model):
    class Meta:
        db_table="MasterBookSolrWrapper"


class BookstoreSolrWrapper(models.Model):
    class Meta:
        db_table="BookstoreSolrWrapper"


class eGazeciarzUser(models.Model):
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
        db_table = 'eGazeciarzUser'

    is_active = True

    REQUIRED_FIELDS = []
