from django.db import models

class MasterBookSolrWrapper(models.Model):
    class Meta:
        db_table="MasterBookSolrWrapper"


class BookstoreSolrWrapper(models.Model):
    class Meta:
        db_table="BookstoreSolrWrapper"
