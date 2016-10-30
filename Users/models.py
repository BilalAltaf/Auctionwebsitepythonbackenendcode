__author__ = 'Bilal'
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime
class Auction_User(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    createdDate = models.DateTimeField (default=timezone.now)
    lastUpdatedDate = models.DateTimeField(default=timezone.now)
    defaultLang = models.CharField(default='en', max_length=2)
