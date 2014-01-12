# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class BookTrack(models.Model):
    masterbook = models.ForeignKey('spistresci.MasterBook', related_name="book_tracks")
    user = models.ForeignKey(User, related_name="book_tracks")
    price = models.IntegerField(null=True, blank=True, verbose_name="Cena")

    class Meta:
        unique_together = (('masterbook', 'user'),)
        db_table = 'BookTrack'
        app_label = 'spistresci'

    def get_price_display(self):
        return u'%.2f zł' % (self.price/100.0,)

class BookTrackNotification(models.Model):
    masterbook = models.ForeignKey('spistresci.MasterBook', related_name="book_track_notifications")
    user = models.ForeignKey(User, related_name="book_track_notifications")
    sent_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'BookTrackNotification'
        app_label = 'spistresci'
