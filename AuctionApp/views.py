
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import translation
from Users.models import *
from Auctions.models import *

# Create your views here.


from django.http import HttpResponseRedirect
def show_index(request):
    return render_to_response("index.html",
                                  {'Homeactive': 'active','Msg' : '' },
                                 context_instance=RequestContext(request)
                                 )
def set_lang(request):
    lang_code = request.POST['lang_code']
    user_language = lang_code
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    request.session['lang_code']= user_language
    if request.user.is_authenticated():
        user = request.user
        try:
            auctionUser = Auction_User.objects.get(user=user)
        except Auction_User.DoesNotExist:
            auctionUser = Auction_User()
            auctionUser.user = user
        auctionUser.defaultLang=user_language
        auctionUser.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def create_data(request):
    catagory = itemType.objects.get(id=6)
    for i in range(1,50):
        user = User.objects.create_user('testuser'+ str(i),'testuser'+ str(i)+'@test.com','abc123')
        user.last_name = 'Last'
        user.first_name = 'First'
        user.save()
        auctionUser = Auction_User()
        auctionUser.user = user
        auctionUser.address = 'Test Address '
        auctionUser.phone = '1234567'
        auctionUser.save()


        objAuction = Auction()
        objAuction.title = 'Test Auction '+ str(i)
        objAuction.minPrice = 1
        objAuction.seller = user
        objAuction.status = 1
        objAuction.itemDescription = 'This is a test'
        objAuction.deadline = datetime.strptime('30/12/2015 20:52','%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
        objAuction.category = catagory
        objAuction.save()

    return HttpResponseRedirect('/')