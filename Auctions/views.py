__author__ = 'Bilal'

from django.contrib.auth.decorators import login_required
import hmac
from hashlib import md5
from AuctionApp.validator import *
from django.db.models import Q
from AuctionApp.views import *
from AuctionApp.models import *
from AuctionApp.emailSender import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# ####### READ ME ##### Active Auctions (Acution.status = 1)..Resolved Auctions (Acution.status = 2)..Banned Auctions (Acution.status = 3)
@login_required
def show_listing(request):
    auctions = Auction.objects.filter(seller = request.user).order_by('-createdDate')
    msg = request.GET.get('msg','')
    return render_to_response("Auctions/listing.html",
                              {'Auctionsactive': 'active','auctions':auctions,'error':'','Msg':msg},
                              context_instance=RequestContext(request))
def show_allAuctions(request,catId=0):
    filedsList =[]
    valuesList =[]
    typesList = []
    NotEqualToList = []
    categories = itemType.objects.all().order_by('typeName')
    msg = request.GET.get('msg','')
    if request.method == "POST":
        category = request.POST['ddlcategory'].strip()
        title = request.POST['txttitle'].strip()
        if( title != ''):
            filedsList.append('title')
            valuesList.append(title)
            typesList.append('icontains')
            NotEqualToList.append(False)
            #itemCategory = itemType.objects.get(id = int(category))
        if( int(category) != 0):
            filedsList.append('category_id')
            valuesList.append(category)
            typesList.append('')
            NotEqualToList.append(False)
        if not request.user.is_superuser:
            filedsList.append('status')
            valuesList.append(3)
            typesList.append('') # Show all to Admin. and only active and Resolved to other users
            NotEqualToList.append(True)

        auctions_list = dynamic_Searchquery(filedsList,typesList,valuesList,'and',NotEqualToList)

        paginator = Paginator(auctions_list, 10) # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            auctions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            auctions = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            auctions = paginator.page(paginator.num_pages)

        return render_to_response("Auctions/allAuctions.html",
                          {'AllAuctionsactive': 'active','auctions':auctions,'error':'','Msg':msg,'categories':categories,'categoryid':int(category),'title':title},
                          context_instance=RequestContext(request))
    else:
        if not request.user.is_superuser:
            filedsList.append('status')
            valuesList.append(3)
            typesList.append('') # Show all to Admin. and only active and Resolved to other users
            NotEqualToList.append(True)

        if catId!=0:
            cate = itemType()
            if cate.exists(catId):
                filedsList.append('category_id')
                valuesList.append(catId)
                typesList.append('')
                NotEqualToList.append(False)
        auctions_list = dynamic_Searchquery(filedsList,typesList,valuesList,'and',NotEqualToList)
        paginator = Paginator(auctions_list, 10) # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            auctions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            auctions = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            auctions = paginator.page(paginator.num_pages)
        return render_to_response("Auctions/allAuctions.html",
                                  {'AllAuctionsactive': 'active','auctions':auctions,'error':'','Msg':msg,'categories':categories,'categoryid':int(catId),},
                                  context_instance=RequestContext(request)

                                  )
def dynamic_Searchquery(fieldsList, typesList, valuesList, operator , notEqualToList):
    queries = []
    for (f, t, v,z) in zip(fieldsList, typesList, valuesList,notEqualToList):
        if v != "" and t == "":
            kwargs = {str('%s' % (f)) : str('%s' % v)}
            if(z):
                queries.append(~Q(**kwargs))
            else:
                queries.append(Q(**kwargs))
        elif  v != "":
            kwargs = {str('%s__%s' % (f,t)) : str('%s' % v)}
            if(z):
                queries.append(~Q(**kwargs))
            else:
                queries.append(Q(**kwargs))

    if len(queries) > 0:
        q = Q()
        for query in queries:
            if operator == "and":
                q = q & query
            elif operator == "or":
                q = q | query
            else:
                q = None

        if q:
            return Auction.objects.filter(q).order_by('-createdDate')

    else:
        return Auction.objects.filter().order_by('-createdDate')
@login_required
def confirm_auction(request):
    AuctionTitle = request.POST['AuctionTitle']
    Deadline = request.POST['Deadline']
    StartingPrice = request.POST['StartingPrice']
    Description = request.POST['Description']
    category = request.POST['Category']
    ItemType = itemType.objects.get(id=category)
    signature = request.POST['signature']
    mykey = mySecKey()
    state = str(AuctionTitle) +'|' + str(Deadline) +'|' + str(StartingPrice) +'|' + str(Description) +'|' + str(category)
    hashed = hmac_md5(mykey,state)
    signature_check = hashed.hexdigest()

    if request.method == "POST":
        if signature == signature_check:
            objAuction = Auction()
            objAuction.title = AuctionTitle
            objAuction.minPrice = StartingPrice
            objAuction.seller = request.user
            objAuction.status = 1
            objAuction.itemDescription = Description
            objAuction.deadline = datetime.strptime(Deadline,'%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
            objAuction.category = ItemType
            objAuction.save()
            emailSender.sendAuctionConfEmail(objAuction.title,request.user.email)
            return HttpResponseRedirect('/myauctions/')
        else:
            return render_to_response("Auctions/confirmAuction.html",
                                          {'Auctionsactive': 'active','error':'Invalid signature operation canceled !!'},
                                          context_instance=RequestContext(request)
                                          )
    else:
         return HttpResponseRedirect('/myauctions/')

@login_required
def create_auction(request):
    if request.method == "POST":
        AuctionTitle = request.POST['txtAuctionTitle']
        Deadline = request.POST['txtDeadline']
        StartingPrice = request.POST['txtStartingPrice']
        Description = request.POST['txtDescription']
        category = request.POST['ddlcategory']
        ItemType = itemType.objects.get(id=category)
        timeDiff = datetime.strptime(Deadline,'%d/%m/%Y %H:%M') - datetime.now()
        hours = timeDiff.total_seconds()/3600 # Difference in hours
        categories = itemType.objects.all().order_by('typeName')
        if int(hours) < 72:
            return render_to_response("Auctions/createAuction.html",
                                      {'Auctionsactive': 'active','myAccountactive':'','categories':categories,'categoryid':int(category), 'AuctionTitle':AuctionTitle,'Deadline':Deadline,'StartingPrice':StartingPrice,'Description':Description, 'error':' Deadline should be greater then 72 hours, your current dearline is ' + str(int(hours)) + ' hours.'},
                                      context_instance=RequestContext(request)
                                      )
        else:

            mykey = mySecKey()
            state = str(AuctionTitle) +'|' + str(Deadline) +'|' + str(StartingPrice) +'|' + str(Description) +'|' + str(category)
            hashed = hmac_md5(mykey,state)
            signature = hashed.hexdigest()
            return render_to_response("Auctions/confirmAuction.html",
                                          {'Auctionsactive': 'active','AuctionTitle':AuctionTitle,'Deadline':Deadline,'StartingPrice':StartingPrice,'Description':Description,'Category':category,'signature':signature},
                                          context_instance=RequestContext(request)
                                          )
    else:
        categories = itemType.objects.all().order_by('typeName')
        return render_to_response("Auctions/createAuction.html",
                                      {'Auctionsactive': 'active','categories':categories},
                                      context_instance=RequestContext(request)
                                      )
def hmac_md5(key, msg):
    return hmac.HMAC(key, msg, md5)

@login_required
def edit_auction(request,auctionId):
    if Auction.exists(auctionId):
        auction = Auction.objects.get(id=auctionId)
        if auction.seller== request.user:
            if request.method == "POST":
                BidVersion = request.POST['BidVersion']
                if float(BidVersion) == float(auction.topBidNo):
                    Description = request.POST['txtDescription']
                    category = request.POST['ddlcategory']
                    ItemType = itemType.objects.get(id=category)
                    auction.itemDescription = Description
                    auction.category = ItemType
                    auction.topBidNo = auction.topBidNo + 1
                    auction.save()
                    return HttpResponseRedirect('/myauctions/?msg=Auction updated successfully!')
                else:
                    categories = itemType.objects.all().order_by('typeName')
                    return render_to_response("Auctions/editAuction.html",
                                              {'Auctionsactive': 'active','categories':categories,'auction':auction,'deadlinedate': auction.deadline.strftime('%d/%m/%Y %H:%M'),'error':'Operation failed because another user has updated(placed a bid) record. Your changes have been lost. Please review their changes before trying again. !!' },
                                              context_instance=RequestContext(request)
                                              )
            else:
                categories = itemType.objects.all().order_by('typeName')
                return render_to_response("Auctions/editAuction.html",
                                              {'Auctionsactive': 'active','categories':categories,'auction':auction,'deadlinedate': auction.deadline.strftime('%d/%m/%Y %H:%M') },
                                              context_instance=RequestContext(request)
                                              )
        else:
            return HttpResponseRedirect('/myauctions/')
    else:
        return HttpResponseRedirect('/myauctions/?msg=Auction does not exist!!')
def view_auction(request,auctionId):
    if Auction.exists(auctionId):
        auction = Auction.objects.get(id=auctionId)
        auctionAllbids = Auction_Bid.objects.filter(auction=auction).order_by('-bidNumber')
        return render_to_response("Auctions/viewAuction.html",
                                      {'AllAuctionsactive': 'active','category':auction.category.typeName,'auctionAllbids':auctionAllbids,'auction':auction,'deadlinedate': auction.deadline.strftime('%d/%m/%Y %H:%M') },
                                      context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/allauctions/?msg=Auction does not exist!!')

@login_required
def bid_auction(request,auctionId):
    if Auction.exists(auctionId):
        auction = Auction.objects.get(id=auctionId)
        if auction.status != 1 :
            return HttpResponseRedirect('/allauctions/?msg=Auction is not Active so cannot be bidded!!')
        else:
            if auction.seller != request.user:
                auctionAllbids = Auction_Bid.objects.filter(auction=auction).order_by('-bidNumber')
                if request.method == "POST":
                    bidAmount = request.POST['txtbidAmount']
                    Comment = request.POST['txtComment']
                    BidVersion = request.POST['BidVersion']
                    InvalidFileds = validate_Bidform(bidAmount,Comment)
                    if len(InvalidFileds) > 0 :
                        return render_to_response("Auctions/bidAuction.html",
                                          {'AllAuctionsactive':'active','category':auction.category.typeName,'auctionAllbids':auctionAllbids,'auction':auction,'deadlinedate': auction.deadline.strftime('%d/%m/%Y %H:%M'),'error' : 'Invalid Field(s) ' + InvalidFileds },
                                          context_instance=RequestContext(request)
                                          )
                    elif float(bidAmount) < auction.minPrice  or float(bidAmount) < auction.topBid or round((float(bidAmount) - auction.minPrice),2)< .01 or round((float(bidAmount) - auction.topBid),2)< .01:
                        return render_to_response("Auctions/bidAuction.html",
                                          {'AllAuctionsactive':'active','category':auction.category.typeName,'bidAmount':bidAmount,'Comment':Comment,'auctionAllbids':auctionAllbids,'auction':auction,'deadlinedate': auction.deadline.strftime('%d/%m/%Y %H:%M'),'error' : 'Minimum bid increment is .01' },
                                          context_instance=RequestContext(request)
                                          )
                    else:
                        mykey = mySecKey()
                        state = str(bidAmount) +'|' + str(Comment) +'|' + str(auctionId) +'|' + str(BidVersion)
                        hashed = hmac_md5(mykey,state)
                        signature = hashed.hexdigest()
                        return render_to_response("Auctions/confirmBid.html",
                                                      {'AllAuctionsactive': 'active','AuctionId':auctionId,'AuctionBid':bidAmount,'comment':Comment,'BidVersion':BidVersion,'signature': signature },
                                                      context_instance=RequestContext(request)
                                                      )
                else:
                    return render_to_response("Auctions/bidAuction.html",
                                                  {'AllAuctionsactive': 'active','category':auction.category.typeName,'auctionAllbids':auctionAllbids,'auction':auction,'deadlinedate': auction.deadline.strftime('%d/%m/%Y %H:%M') },
                                                  context_instance=RequestContext(request)
                                                  )
            else:
                return HttpResponseRedirect('/allauctions/?msg=you can not bid on your own auction!!')
    else:
        return HttpResponseRedirect('/allauctions/?msg=Auction does not exist!!')
@login_required
def confirm_bid(request):
    bidAmount = request.POST['AuctionBid']
    Comment = request.POST['comment']
    AuctionId = request.POST['AuctionId']
    signature = request.POST['signature']
    BidVersion = request.POST['BidVersion']
    mykey = mySecKey()
    state = str(bidAmount) +'|' + str(Comment)+'|' + str(AuctionId) +'|' + str(BidVersion)
    hashed = hmac_md5(mykey,state)
    signature_check = hashed.hexdigest()
    auction = Auction.objects.get(id=AuctionId)
    auctionAllbids = Auction_Bid.objects.filter(auction=auction).order_by('-bidNumber')
    if request.method == "POST":
        if signature == signature_check:
            if float(BidVersion) == float(auction.topBidNo):
                if(auction.status == 1):
                    if( float(auction.topBid) < float(bidAmount) and float(auction.minPrice) < float(bidAmount)):
                        if(auction.deadline > datetime.now()):
                            auctionbid = Auction_Bid()
                            auctionbid.bidUser = request.user
                            auctionbid.auction = auction
                            auctionbid.comment = Comment
                            auctionbid.amount = bidAmount
                            auctionbid.bidNumber = auction.topBidNo + 1
                            auctionbid.bidDate = datetime.now()
                            auctionbid.save()

                            #Implementing Soft Deadlines If user bid with in 5 mins of deadline end, deadline will be extended for extra 5 mins
                            timeDiff = auction.deadline - datetime.now()
                            Diffminutes = timeDiff.total_seconds()/60 # Difference in Minures
                            if (Diffminutes < 5):
                                auction.deadline = auction.deadline + timedelta(minutes = 5)

                            auction.topBidNo = auction.topBidNo + 1
                            auction.topBid = bidAmount
                            auction.save()

                            emailSender.sendBidConfEmail(auction.title,bidAmount,request.user.email)
                            emailSender.sendBidEmailToSeller(auction.title,bidAmount,auction.seller.email)
                            if float(BidVersion) > 0:
                                if Auction_Bid.Exist(auction.id,float(BidVersion)):
                                    PrevUser = Auction_Bid.loadByBidVersion(auction.id,float(BidVersion)).bidUser
                                    emailSender.sendBidEmailToPreviousBidder(auction.title,bidAmount,PrevUser.email)
                            return HttpResponseRedirect('/bidauction/'+str(AuctionId)+'/')
                        else:
                            return HttpResponseRedirect('/allauctions/?msg=Auction deadline is over, so it cannot be bidded anymore.!!')
                    else:
                        return HttpResponseRedirect('/allauctions/?msg=Bid Amount should br greated than top Bid and minimum price !!')
                else:
                    return HttpResponseRedirect('/allauctions/?msg=Auction is not Active so cannot be bidded!!')
            else:
                return render_to_response("Auctions/bidAuction.html",
                                          {'AllAuctionsactive': 'active','category':auction.category.typeName,'auctionAllbids':auctionAllbids,'auction':auction,'deadlinedate': auction.deadline.strftime('%d/%m/%Y %H:%M'),'error':'Concurrency Issue: Operation failed because another user has updated(placed a bid) record. Your changes have been lost. Please review their changes before trying again. !!'},
                                          context_instance=RequestContext(request)
                                          )
        else:
            return render_to_response("Auctions/bidAuction.html",
                                          {'AllAuctionsactive': 'active','category':auction.category.typeName,'auctionAllbids':auctionAllbids,'auction':auction,'deadlinedate': auction.deadline.strftime('%d/%m/%Y %H:%M'),'error':'Invalid signature operation canceled !!'},
                                          context_instance=RequestContext(request)
                                          )
    else:
         return HttpResponseRedirect('/myauctions/')
@login_required
def ban_auction(request,auctionId):
    if request.user.is_superuser:
        mykey = mySecKey()
        state = str(auctionId)
        hashed = hmac_md5(mykey,state)
        signature_check = hashed.hexdigest()
        auction = Auction.objects.get(id=auctionId)
        #auctionAllbids = Auction_Bid.objects.filter(auction=auction).order_by('-bidNumber')
        if request.method == "POST":
            signature = request.POST['signature']
            if signature == signature_check:
                auction.status = 3
                auction.save()
                emailSender.NotifySellerBanAuction(auction.title,auction.seller.email)
                auctionAllbids = Auction_Bid.objects.filter(auction=auction)

                # get Distinct Emails so that a bidder who have bidded more than one time should not get more then one email.
                EmailList = map(lambda x: x.bidUser.email, auctionAllbids)
                DistinctEmails = set(EmailList)

                # Inform all Bidders who placed a bid on this Auction
                for Email in DistinctEmails:
                    emailSender.NotifyBiddersBanAuction(auction.title,Email)
                return HttpResponseRedirect('/allauctions/?msg=Auction Banned successfully!!')
            else:
                HttpResponseRedirect('/allauctions/?msg=Invalid signature operation canceled !!')
        else:
             return render_to_response("Auctions/banAuction.html",
                                              {'AllAuctionsactive': 'active','signature':signature_check,'auctionId':auctionId},
                                              context_instance=RequestContext(request)
                                              )
    return HttpResponseRedirect('/allauctions/')
def mySecKey():
    return '44b9762d7f3f43d7954a0e833f7b4b23'
def validate_Bidform(BidAmound,comment):
    InvalidFiledsList = []
    if not validator.isValidDecimalwithTwoDecimal(BidAmound):
        InvalidFiledsList.append('Bid Amound')
    if not validator.isValidText(comment):
        InvalidFiledsList.append('Comment')
    if len(InvalidFiledsList) > 0 :
        InvalidFileds = ','.join(map(str, InvalidFiledsList))
        return InvalidFileds
    else:
        return ''