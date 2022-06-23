from django.db import models

# Create your models here.
class Portfolio(models.Model):
    title = models.CharField(max_length=200, blank=False, default='')
    artist = models.CharField(max_length=200, blank=False, default='')
    medium = models.CharField(max_length=200, blank=False, default='')
    published = models.BooleanField(default=False)