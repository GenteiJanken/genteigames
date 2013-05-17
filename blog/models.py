from django.db import models
from datetime import datetime

class Post(models.Model):
    head = models.CharField(max_length=60)
    date = models.DateField(default=datetime.now())
    body = models.TextField() 


    def __unicode__(self):
        return self.head
