from django.db import models

class Address(models.Model):
    email = models.EmailField()
    date = models.DateField()

    class Meta:
    	db_table="Address"
    
    def __unicode__(self):
        return u'%s %s' % (self.email, self.date)

