__author__ = 'Bilal'

from django.http import HttpResponse
from  Auctions.models import *
import base64
from Auctions.models import Auction
from serializer import *
from AuctionApp.emailSender import *

from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login
from AuctionApp.validator import *
from Users.models import *
from rest_framework import status
from django.http import JsonResponse

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(['GET'])
@renderer_classes([JSONRenderer,])
def allCategories(request):
    categories = itemType.objects.all().order_by('typeName')
    serializer = CategorySerializer(categories, many=True)
    return  JsonResponse({'statusCode':status.HTTP_200_OK,'data':serializer.data})

@api_view(['GET'])
@renderer_classes([JSONRenderer,])
def allAuctions(request):
    auctions = Auction.objects.all()
    serializer = AuctionSerializer(auctions, many=True)
    return  JsonResponse({'statusCode':status.HTTP_200_OK,'data':serializer.data})
    #return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@renderer_classes([JSONRenderer,])
def viewauctions(request,auctionId):
    try:
        auction = Auction.objects.get(id=auctionId)
        auctionAllbids = Auction_Bid.objects.filter(auction=auction).order_by('-bidNumber')
    except Auction.DoesNotExist:
        return  JsonResponse({'statusCode':status.HTTP_404_NOT_FOUND,'data':{'Message':'Auction Not Found!'}})

    serializer = AuctionSerializer(auction)
    bidSerializer = AuctionBidSerializer(auctionAllbids, many=True)
    return  JsonResponse({'statusCode':status.HTTP_200_OK,'data':{"Auction": serializer.data,'Biding': bidSerializer.data}})

@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def bidauctions(request,auctionId):
    try:
        auction = Auction.objects.get(id=auctionId)
    except Auction.DoesNotExist:
        return  JsonResponse({'statusCode':status.HTTP_404_NOT_FOUND,'data':{'Message':'Auction Not Found!'}})
    if request.method == 'GET':
        serializer =  AuctionSerializer(auction)
        return JSONResponse({'statusCode':status.HTTP_200_OK,'data':serializer.data})
    elif request.method == 'POST':
        data = request.data

        Auctionid = data.get('Auctionid')
        BidVersion = data.get('BidVersion')
        bidAmount  = data.get('bidAmount')
        Comment  = data.get('Comment','')
        print Auctionid
        #print validator.isValidId(Auctionid)
        if not Auctionid:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Auctionid is not provider.'}})
        if not BidVersion and BidVersion != 0:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Auctionid is not provider.'}})
        if not bidAmount:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Auctionid is not provider.'}})
        if Auction.exists(Auctionid):
            auction = Auction.objects.get(id=Auctionid)
        else:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'invalid Auctionid.'}})
        if auction.status != 1:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Auction is not active so cannot be bidded.'}})
        elif auction.seller == request.user:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'You cannot bid on your own Action.'}})
        elif float(bidAmount) - float(auction.topBid) < .01 or float(bidAmount) - float(auction.minPrice) < .01:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Difference between bidAmount and TopBid/MinPrice should be at least .01 .'}})

        elif auction.deadline < datetime.now():
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':' Auction deadline is over, so cannot be bidded anymore.'}})
        elif BidVersion != auction.topBidNo:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Concurrency Issue: Operation failed because another user has updated(placed a bid) record. Your changes have been lost. Please review their changes before trying again.'}})


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
        return  JsonResponse({'statusCode':status.HTTP_200_OK,'data':{'Message':'Auction Bid Placed successfully for auction ' + auction.title + ' with amount ' + str(bidAmount)}})

#Get Auctions by Category.
@api_view(['GET'])
@renderer_classes([JSONRenderer,])
def getAuctionsByCat(request,categoryId):
    filedsList =[]
    valuesList =[]
    typesList = []
    NotEqualToList = []
    try:
        if categoryId!=0:
            cate = itemType()
            if cate.exists(categoryId):
                filedsList.append('category_id')
                valuesList.append(categoryId)
                typesList.append('')
                NotEqualToList.append(False)
        auctions_list = dynamic_Searchquery(filedsList,typesList,valuesList,'and',NotEqualToList)

    except Auction.DoesNotExist:
        return  JsonResponse({'statusCode':status.HTTP_404_NOT_FOUND,'data':{'Message':'Auction Not Found!'}})

    serializer = AuctionSerializer(auctions_list, many=True)
    return JsonResponse({'statusCode':status.HTTP_200_OK,'data':serializer.data})
    #return Response(serializer.data)

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

def validate_form(email,firstName,lastName,username,password,conformpassword):
    InvalidFiledsList = []
    if not validator.isValidEmail(email):
        InvalidFiledsList.append('Email')
    if not validator.isValidName(firstName):
        InvalidFiledsList.append('First Name')
    if not validator.isValidName(lastName):
        InvalidFiledsList.append('Last Name')
    if not validator.isValidUserName(username):
        InvalidFiledsList.append('User Name')
    if not validator.isValidPassword(password):
        InvalidFiledsList.append('Password')
    if  password != conformpassword:
        InvalidFiledsList.append('Password and confirm Password does not match')
    if len(InvalidFiledsList) > 0 :
        InvalidFileds = ','.join(map(str, InvalidFiledsList))
        return InvalidFileds
    else:
        return ''

#Create Auction
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def createAuction(request):
    AuctionTitle = request.POST['AuctionTitle']
    Deadline = request.POST['Deadline']
    StartingPrice = request.POST['StartingPrice']
    Description = request.POST['Description']
    category = request.POST['Category']
    ItemType = itemType.objects.get(id=category)
    if not AuctionTitle:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'AuctionTitle is not provider.'}})
    if not Deadline:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Deadline is not provider.'}})
    if not StartingPrice:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'StartingPrice is not provider.'}})
    if not Description:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Description is not provider.'}})
    if not category:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'category is not provider.'}})

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
    return JsonResponse({'statusCode':status.HTTP_200_OK,'data':{'Message':'Auction Created Sussessfully.'}})
#Regester User
@api_view(['POST'])
def regesterUser(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    firstName  = data.get('firstName')
    lastName  = data.get('lastName')
    conformpassword = data.get('conformpassword')
    email = data.get('email')
    phone  = data.get('phone')
    address  = data.get('address')
    if not username:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'username is not provider.'}})
    if not password:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'password is not provider.'}})
    if not firstName:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'firstName is not provider.'}})
    if not lastName:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'lastName is not provider.'}})
    if not conformpassword:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'conformpassword is not provider.'}})
    if not email:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'email is not provider.'}})

    if User.objects.filter(username=username).exists():
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'User Name Exist, please choose a different user name.'}})
    else:
        InvalidFileds = validate_form(email,firstName,lastName,username,password,conformpassword)
        if len(InvalidFileds) > 0 :
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Invalid Field(s) ' + InvalidFileds}})
        else:
            user = User.objects.create_user(username,email,password)
            user.last_name = lastName
            user.first_name = firstName
            user.save()
            auctionUser = Auction_User()
            auctionUser.user = user
            auctionUser.address = address
            auctionUser.phone = phone
            auctionUser.save()
            return JsonResponse({'statusCode':status.HTTP_200_OK,'data':{'Message':'User '+firstName + ' ' +lastName+' regesterd successfully'}})

#Get User Auctions
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getMyAuctions(request):
    try:
        auctions_list = Auction.objects.filter(seller = request.user).order_by('-createdDate')
    except Auction.DoesNotExist:
        return  JsonResponse({'statusCode':status.HTTP_404_NOT_FOUND,'data':{'Message':'Auction Not Found!'}})

    serializer = AuctionSerializer(auctions_list, many=True)
    return JsonResponse({'statusCode':status.HTTP_200_OK,'data':serializer.data})

#Regester User
@api_view(['POST'])
def loginUser(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    if not username:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'username is not provider.'}})
    if not password:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'password is not provider.'}})
    #user = authenticate(username=username,password=password)
    user = User.objects.get(username=username)
    if user is not None:
            if user.is_active:

                hd_value = "%s:%s" % (username, password)
                try:
                    auctionUser = Auction_User.objects.get(user=user)
                except Auction_User.DoesNotExist:
                    auctionUser = Auction_User()
                return JSONResponse({'statusCode':status.HTTP_200_OK,'data':{'Token':"Basic "+ base64.b64encode(hd_value),'IsSuperUser':user.is_superuser,'firstName':user.first_name,'lastName':user.last_name,'username':request.user.username,'email':user.email,'address':auctionUser.address,'phone':auctionUser.phone}})
            else:
                return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'User inactive'}})
    else:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Invalid Login credentials'}})

#Ban Auction Admin Only.
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def banAuction(request,auctionId):
    if request.user.is_superuser:
        auction = Auction.objects.get(id=auctionId)
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
        return  JsonResponse({'statusCode':status.HTTP_200_OK ,'data':{'Message':'Auction Banned Successfully.'}})
    else:
        return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Only Superior User can ban auction.'}})


#Edit User
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def editUser(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        try:
            auctionUser = Auction_User.objects.get(user=user)
        except Auction_User.DoesNotExist:
            auctionUser = Auction_User()
        return JSONResponse({'statusCode':status.HTTP_200_OK,'data':{'firstName':user.first_name,'lastName':user.last_name,'username':request.user.username,'email':request.user.email,'address':auctionUser.address,'phone':auctionUser.phone,'password':'********'}})
    elif request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        firstName  = data.get('firstName')
        lastName  = data.get('lastName')
        conformpassword = data.get('conformpassword')
        email = data.get('email')
        phone  = data.get('phone')
        address  = data.get('address')
        if not username:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'username is not provider.'}})
        if not password:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'password is not provider.'}})
        if not firstName:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'firstName is not provider.'}})
        if not lastName:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'lastName is not provider.'}})
        if not conformpassword:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':'conformpassword is not provider.'})
        if not email:
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'email is not provider.'}})

        if not User.objects.filter(username=username).exists():
            return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'User Does not Name Exist'}})
        else:
            if password != '********': # Change it to "  if not check_password(request.POST['txtpassword']) "
                user.set_password(password)
            InvalidFileds = validate_form(email,firstName,lastName,username,password,conformpassword)
            if len(InvalidFileds) > 0 :
                return  JsonResponse({'statusCode':status.HTTP_400_BAD_REQUEST,'data':{'Message':'Invalid Field(s) ' + InvalidFileds}})
            else:
                user.email = email
                user.last_name = lastName
                user.first_name = firstName
                user.save()
                try:
                    auctionUser = Auction_User.objects.get(user=user)
                except Auction_User.DoesNotExist:
                    auctionUser = Auction_User()
                    auctionUser.user = user
                auctionUser.address = address
                auctionUser.phone = phone
                auctionUser.save()
                return JsonResponse({'statusCode':status.HTTP_200_OK,'data':{'Message':'User '+firstName + ' ' +lastName+' Updated successfully'}})

@api_view(['GET'])
def getUser(request,userId):
    try:
        try:
            user = User.objects.get(id=userId)
            auctionUser = Auction_User.objects.get(user=user)
        except user.DoesNotExist:
            return  JsonResponse({'statusCode':status.HTTP_404_NOT_FOUND,'data':'User Not Found!'})

    except Auction_User.DoesNotExist:
        auctionUser = Auction_User()
    return JSONResponse({'statusCode':status.HTTP_200_OK,'data':{'IsSuperUser':user.is_superuser,'firstName':user.first_name,'lastName':user.last_name,'username':request.user.username,'email':request.user.email,'address':auctionUser.address,'phone':auctionUser.phone}})
