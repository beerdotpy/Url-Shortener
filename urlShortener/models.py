from django.db import models
import random
import string
import datetime
from django.core.validators import URLValidator

class User(models.Model):
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)

class URL(models.Model):
    user = models.ForeignKey(User)
    original = models.CharField(max_length=255)
    shortenURL = models.TextField(validators=[URLValidator()])
    isActive = models.BooleanField(default = True)
    
class Click(models.Model):
    url = models.ForeignKey(URL)
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        #On save, update timestamps 
        if not self.id:
            self.timestamp = datetime.datetime.today()
        return super(Click, self).save(*args, **kwargs)
