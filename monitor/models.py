from __future__ import unicode_literals
from django.db import models

class UpdateStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    manual = models.IntegerField(null=True, blank=True)
    partial = models.IntegerField(null=True, blank=True)
    finished = models.IntegerField(null=True, blank=True)
    success = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'UpdateStatus'

class UpdateStatusService(models.Model):
    id = models.IntegerField(primary_key=True)
    update_status = models.ForeignKey(UpdateStatus, null=True, blank=True)
    service_name = models.ForeignKey("Service", null=True, db_column='service_name', blank=True)
    success = models.IntegerField(null=True, blank=True)
    checksum = models.CharField(max_length=32L, blank=True)
    offers = models.IntegerField(null=True, blank=True)
    offers_parsed = models.IntegerField(null=True, blank=True)
    offers_new = models.IntegerField(null=True, blank=True)
    offers_promotion = models.IntegerField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    fetch_start = models.DateTimeField(null=True, blank=True)
    fetch_end = models.DateTimeField(null=True, blank=True)
    parse_start = models.DateTimeField(null=True, blank=True)
    parse_end = models.DateTimeField(null=True, blank=True)
    final_start = models.DateTimeField(null=True, blank=True)
    final_end = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'UpdateStatusService'

class Service(models.Model):
    name = models.CharField(max_length=32L, primary_key=True)
    website = models.CharField(max_length=32L, blank=True)
    class Meta:
        db_table = 'Service'
