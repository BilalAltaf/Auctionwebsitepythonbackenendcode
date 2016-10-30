__author__ = 'Bilal'

from django.forms import widgets
from rest_framework import serializers
from  Auctions.models import *
from Users.models import *
from AuctionApp.models import *

class BidUserSerializer(serializers.Serializer):
    UserId = serializers.CharField(source="id")
    FirstName = serializers.CharField(source="first_name")
    LastName = serializers.CharField(source="last_name")
    Email = serializers.CharField(source="email")
    class Meta:
        model = User
        fields = ('FirstName','LastName' , 'Email' , 'UserId')

class AuctionSerializer(serializers.ModelSerializer):
    seller = BidUserSerializer()
    #winner = BidUserSerializer()
    class Meta:
        model = Auction
        fields = ('id', 'title', 'itemDescription', 'minPrice','topBid', 'topBidNo', 'deadline','seller','category','status','winner','createdDate')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = itemType
        fields = ('id', 'typeName')

class AuctionBidSerializer(serializers.ModelSerializer):
    bidUser= BidUserSerializer()
    class Meta:
        model = Auction_Bid
        fields = ('bidUser', 'amount', 'bidNumber', 'comment','bidDate')
