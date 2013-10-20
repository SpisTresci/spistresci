from django.db import models
from django.contrib.auth.models import User
from spistresci.models import MasterBook

class BookTrack(models.Model):
    masterbook = models.ForeignKey(MasterBook, related_name="book_tracks")
    user = models.ForeignKey(User, related_name="book_tracks")
    price = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'BookTrack'

class BookTrackNotification(models.Model):
    masterbook = models.ForeignKey(MasterBook, related_name="book_track_notifications")
    user = models.ForeignKey(User, related_name="book_track_notifications")
    sent_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'BookTrackNotification'
