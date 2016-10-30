__author__ = 'Bilal'

from django.contrib.auth.models import User
from AuctionApp.models import *
from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
from django.db.models import Q
class Auction(models.Model):
    seller = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    itemDescription = models.CharField(max_length=300)
    minPrice = models.FloatField(default=0)
    topBid = models.FloatField(default=0)
    topBidNo = models.IntegerField(default=0)
    category = models.ForeignKey(itemType)
    status = models.IntegerField(default=1)
    winner = models.CharField(max_length=30,default='')
    deadline = models.DateTimeField (default= timezone.now)
    createdDate = models.DateTimeField (default=timezone.now)
    lastModifiedDate = models.DateTimeField(default=timezone.now)
    @classmethod
    def exists(cls, Id):
        return len(cls.objects.filter(id=Id)) > 0


class Auction_Bid(models.Model):
    auction = models.ForeignKey(Auction)
    bidUser = models.ForeignKey(User)
    amount =models.FloatField(default=0)
    bidNumber = models.IntegerField(default=0)
    comment = models.CharField(max_length=300)
    bidDate = models.DateTimeField (default=timezone.now)

    @classmethod
    def loadByBidVersion(cls, auctionId,bidVersion):
        return Auction_Bid.objects.filter(Q(auction_id=auctionId) & Q(bidNumber = bidVersion)).order_by('-id')[0]
    @classmethod
    def Exist(cls, auctionId,bidVersion):
        return len(cls.objects.filter(Q(auction_id=auctionId) & Q(bidNumber = bidVersion))) > 0