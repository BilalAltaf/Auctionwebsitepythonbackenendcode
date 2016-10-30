from django.test import TestCase,RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core import mail
from Auctions.views import *
from Auctions.models import *
from django.test import Client
# Create your tests here.
class WebProjectApp_Test(TestCase):
    #TR1.1 database fxture should be used when executing your functional tests.
      fixtures = ['My_Test_Data.json']
      def setUp(self):
        self.factory = RequestFactory()

      #TR2.1 automated test for UC3
      def test_CreateAuction(self):
        print '************************************** TR2.1 ***************************************************************'
        print 'Creating an Auction!'
        AuctionTitle = 'My IPhone'
        Deadline = '25/04/2016 00:09'
        StartingPrice = 10
        Description = 'It is Almost new '
        Category = 1
        mykey = mySecKey()
        state = str(AuctionTitle) +'|' + str(Deadline) +'|' + str(StartingPrice) +'|' + str(Description) +'|' + str(Category)
        hashed = hmac_md5(mykey,state)
        signature = hashed.hexdigest()

        client = Client()
        client.login(username='waleed',password='abc123')
        resp = client.post('/confirmauction/', {'AuctionTitle':AuctionTitle, 'Deadline':Deadline, 'StartingPrice':StartingPrice, 'Description':Description, 'Category':Category, 'signature':signature})

        auction = Auction.objects.get(id=1)
        self.assertRedirects(resp,'/myauctions/')
        print ' New Auction Created '
        print ' Title : ' + auction.title
        print ' Description : ' + auction.itemDescription
        self.client.logout()

      #TR2.2 Automated test for UC6 Bid
      def test_BidAuction(self):
        print '************************************** TR2.2 ***************************************************************'

        client = Client()
        client.login(username='hamza',password='abc123')

        # Data for Posting to Bidding page
        bidAmount = 60
        Comment = 'This is a test'
        AuctionId = 3
        BidVersion = 0
        mykey = mySecKey()
        state = str(bidAmount) +'|' + str(Comment)+'|' + str(AuctionId) +'|' + str(BidVersion)
        hashed = hmac_md5(mykey,state)
        signature = hashed.hexdigest()

        print 'Bidding an Auction!'

        resp = client.post('/confirmbid/', {'AuctionBid':bidAmount, 'comment':Comment, 'AuctionId':AuctionId, 'BidVersion':BidVersion, 'signature':signature})

        auctionbid = Auction_Bid.objects.get(id=1)
        self.assertRedirects(resp,'/bidauction/'+str(AuctionId)+'/')
        print ' New Auction Created '
        print 'Auction Title : ' + auctionbid.auction.title
        print 'Bid Amount : ' + str(auctionbid.amount)

        client.logout()

      #TR2.3 Automated test for testing concurrency when bidding
      def test_BiddingConcurrency(self):

        client = Client()
        client.login(username='waleed',password='abc123')

        print '************************************** TR2.3 ***************************************************************'

        # Bidding an Auction with BidVersion = 0
        bidAmount = 49
        Comment = 'This is a test'
        AuctionId = 1
        BidVersion = 0
        mykey = mySecKey()
        state = str(bidAmount) +'|' + str(Comment)+'|' + str(AuctionId) +'|' + str(BidVersion)
        hashed = hmac_md5(mykey,state)
        signature = hashed.hexdigest()

        resp = client.post('/confirmbid/', {'AuctionBid':bidAmount, 'comment':Comment, 'AuctionId':AuctionId, 'BidVersion':BidVersion, 'signature':signature})

        #Successful bid and redirect to main page
        self.assertRedirects(resp,'/bidauction/'+str(AuctionId)+'/')
        self.failUnlessEqual(resp.status_code , 302)

        #Bidding Again With Same version i,e version = 0
        bidAmount = 50
        mykey = mySecKey()
        state = str(bidAmount) +'|' + str(Comment)+'|' + str(AuctionId) +'|' + str(BidVersion)
        hashed = hmac_md5(mykey,state)
        signature = hashed.hexdigest()

        resp = client.post('/confirmbid/', {'AuctionBid':bidAmount, 'comment':Comment, 'AuctionId':AuctionId, 'BidVersion':BidVersion, 'signature':signature})

        # There will be an error message with text "Concurrency Issue:" as we are using same version.
        self.assertContains(resp,"Concurrency Issue:")

        # Now changing version and againg testing now we will be able to bid.
        bidAmount = 60
        BidVersion = 1
        mykey = mySecKey()
        state = str(bidAmount) +'|' + str(Comment)+'|' + str(AuctionId) +'|' + str(BidVersion)
        hashed = hmac_md5(mykey,state)
        signature = hashed.hexdigest()

        resp = client.post('/confirmbid/', {'AuctionBid':bidAmount, 'comment':Comment, 'AuctionId':AuctionId, 'BidVersion':BidVersion, 'signature':signature})

        # #Successful bid and redirect to main page. No Concurrency Issue now
        self.assertRedirects(resp,'/bidauction/'+str(AuctionId)+'/')
        self.failUnlessEqual(resp.status_code , 302)

        auctionbid = Auction_Bid.objects.get(id=2)
        #self._assert_template_used(resp,'bidAuction.html')
        print ' New Auction Created '
        print 'Auction Title : ' + auctionbid.auction.title
        print 'Bid Amount : ' + str(auctionbid.amount)

        client.logout()