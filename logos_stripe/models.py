from django.db import models

class bookshop(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=40)

    class Meta:
        db_table="bookshop"
    
    def __unicode__(self):
        return u'%s %s' % (self.name, self.address)



