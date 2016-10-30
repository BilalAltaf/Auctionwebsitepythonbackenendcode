__author__ = 'Bilal'
from django.core.mail import send_mail
class emailSender():
    @staticmethod
    def sendAuctionConfEmail(title, emailAddress):
        body = " New Auction "+ title +" Created Successfully \n\n Best Regards \n YAAS Team"
        from_email = 'noreply@yaas.com'
        to_email = emailAddress
        send_mail('New Auction conformation',body, from_email, [to_email,], fail_silently=False)

    @staticmethod
    def sendBidConfEmail(auctionTitle,amount, emailAddress):
        body = " Your Bid on "+ auctionTitle +" with amount "+ str(amount) +" is placed Successfully \n\n Best Regards \n YAAS Team"
        from_email = 'noreply@yaas.com'
        to_email = emailAddress
        send_mail('New Bid Placed',body, from_email, [to_email,], fail_silently=False)

    @staticmethod
    def sendBidEmailToSeller(auctionTitle,amount, emailAddress):
        body = " New Bid on your Auction "+ auctionTitle +" with amount "+ str(amount)  +" is placed Successfully \n\n Best Regards \n YAAS Team"
        from_email = 'noreply@yaas.com'
        to_email = emailAddress
        send_mail('New Bid Placed',body, from_email, [to_email,], fail_silently=False)

    @staticmethod
    def sendBidEmailToPreviousBidder(auctionTitle,amount, emailAddress):
        body = " New Bid on an Auction("+ auctionTitle +") with amount "+ str(amount)  +", Previously Bidded by you is placed \n\n Best Regards \n YAAS Team"
        from_email = 'noreply@yaas.com'
        to_email = emailAddress
        send_mail('New Bid Placed',body, from_email, [to_email,], fail_silently=False)

    @staticmethod
    def NotifySellerBanAuction(auctionTitle, emailAddress):
        body = " Your Auction("+ auctionTitle +") is Banned, Please contact Administrator for any query. \n\n Best Regards \n YAAS Team"
        from_email = 'noreply@yaas.com'
        to_email = emailAddress
        send_mail('New Bid Placed',body, from_email, [to_email,], fail_silently=False)

    @staticmethod
    def NotifyBiddersBanAuction(auctionTitle, emailAddress):
        body = "Auction("+ auctionTitle +") is Banned, Please contact Administrator for any query. \n\n Best Regards \n YAAS Team"
        from_email = 'noreply@yaas.com'
        to_email = emailAddress
        send_mail('New Bid Placed',body, from_email, [to_email,], fail_silently=False)

    @staticmethod
    def sendBidWinnerEmail(auctionTitle,amount, emailAddress,lastName):
        body = "Dear "+ lastName +",\nCongratulations, Your have won the Auction "+ auctionTitle +" with amount "+ str(amount) +" , Please contact Administrator for any further query. \n\n Best Regards \n YAAS Team"
        from_email = 'noreply@yaas.com'
        to_email = emailAddress
        send_mail('Your have won the Auction',body, from_email, [to_email,], fail_silently=False)

    @staticmethod
    def NotifyResolvedAuction(auctionTitle, emailAddress,lastName):
        body = "Dear "+ lastName +",\n Auction("+ auctionTitle +") is now resolved, Please contact Administrator for any query. \n\n Best Regards \n YAAS Team"
        from_email = 'noreply@yaas.com'
        to_email = emailAddress
        send_mail('Auction Resolved',body, from_email, [to_email,], fail_silently=False)