from django.db import models

class DataTable(models.Model):
    email = models.EmailField()
    date = models.DateField()
    
    def __unicode__(self):
        return u'%s %s' % (self.email, self.date)

# Create your models here.
