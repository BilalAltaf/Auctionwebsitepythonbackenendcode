__author__ = 'Bilal'

from django_cron import CronJobBase, Schedule
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils import timezone
from Auctions.models import *
from django.db.models import Max
from AuctionApp.emailSender import *
class AuctionCronJob(CronJobBase):

    RUN_EVERY_MINS = 1
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'Auction.my_cron_job'    # this should be unique code

    def do(self):
        print "Auction Cron Job is running!"
        auctions = Auction.objects.all()
        for auction in auctions:
              if auction.deadline < datetime.now() and auction.status == 1 :

                #Assuming that the last bidder will have the highest amount

                top_bidid = Auction_Bid.objects.filter(Q(auction=auction)).aggregate(Max('id'))
                top_Bidrecord = Auction_Bid.objects.get(id = int(top_bidid['id__max']))

                auction.status=2 # Resolved Auction is an auction with status = 2
                auction.winner = top_Bidrecord.bidUser.username
                auction.save()

                emailSender.sendBidWinnerEmail(auction.title,top_Bidrecord.amount,top_Bidrecord.bidUser.email,top_Bidrecord.bidUser.last_name)

                allAuction_Bid = Auction_Bid.objects.filter(Q(auction=auction))
                for auctionbid in allAuction_Bid:
                   emailSender.NotifyResolvedAuction(auction.title,auctionbid.bidUser.email,auctionbid.bidUser.last_name)

