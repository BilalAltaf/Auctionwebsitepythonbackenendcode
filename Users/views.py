__author__ = 'Bilal'
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Template, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from AuctionApp.AuctionAppfy import content_to_html, html_to_content
from Users.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from AuctionApp.validator import *
from django.utils import translation
# Create your views here.
def register_user(request):

     if request.method == "POST":
        username = request.POST['txtuserName']
        password = request.POST['txtpassword']
        firstName = request.POST['txtfName']
        lastName = request.POST['txtlName']
        conformpassword = request.POST['txtConfPassword']
        email = request.POST['txtEmail']
        phone = request.POST['txtphone']
        address = request.POST['txtAddress']
        if User.objects.filter(username=username).exists():
            return render_to_response("Users/register.html",
                                      {'error' : 'User Name Exist, please choose a different user name ','username':username,'firstName':firstName,'lastName':lastName,'email':email,'phone':phone,'address':address },
                                      context_instance=RequestContext(request)
                                      )
        else:
            InvalidFileds = validate_form(email,firstName,lastName,username,password,conformpassword)
            if len(InvalidFileds) > 0 :
                return render_to_response("Users/register.html",
                                      {'Registeractive':'active','error' : 'Invalid Field(s) ' + InvalidFileds },
                                      context_instance=RequestContext(request)
                                      )

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

                return HttpResponseRedirect('/')
     else:
         return render_to_response("Users/register.html",
                                  {'Registeractive':'active'},
                                  context_instance=RequestContext(request))

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

def login_user(request):
    if request.method == "POST":
        username = request.POST['txtuserName']
        password = request.POST['txtpassword']
        nextTo = request.GET.get('next', '/')
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                set_lang(request)
                return HttpResponseRedirect(nextTo)
            else:
                return render_to_response("Users/login.html",
                                  {'errormessage':'User inactive'},
                                  context_instance=RequestContext(request))

        else:
            return render_to_response("Users/login.html",
                                  {'errormessage':'Invalid Login credentials'},
                                  context_instance=RequestContext(request))


    else:
        if request.user.is_authenticated():
            logout(request)
            request.session.flush()
            return render_to_response("Users/login.html",
                                  {},
                                  context_instance=RequestContext(request)
                                  )
        else:
            return render_to_response("Users/login.html",
                                  {},
                                  context_instance=RequestContext(request)

                                 )
def set_lang(request):
    if request.user.is_authenticated():
        user = request.user
        try:
            auctionUser = Auction_User.objects.get(user=user)
        except Auction_User.DoesNotExist:
            auctionUser = Auction_User()
            auctionUser.user = user
            auctionUser.save()
        translation.activate(auctionUser.defaultLang)
        request.session[translation.LANGUAGE_SESSION_KEY] = auctionUser.defaultLang
        request.session['lang_code']= auctionUser.defaultLang

@login_required
def edit_account(request):
    if request.method == "POST":
        if (request.user.username == request.POST['txtuserName']):
            user = User.objects.get(username=request.user.username)
            password = request.POST['txtpassword']
            username = request.POST['txtuserName']
            firstName = request.POST['txtfName']
            lastName = request.POST['txtlName']
            conformpassword = request.POST['txtConfPassword']
            email = request.POST['txtEmail']
            phone = request.POST['txtphone']
            address = request.POST['txtAddress']

            InvalidFileds = validate_form(email,firstName,lastName,username,password,conformpassword)

            if request.POST['txtpassword'] != '********': # Change it to "  if not check_password(request.POST['txtpassword']) "
                user.set_password(request.POST['txtpassword'])
            if len(InvalidFileds) > 0 :
                return render_to_response("Users/editAccount.html",
                                      {'Registeractive':'active','error' : 'Invalid Field(s) ' + InvalidFileds },
                                      context_instance=RequestContext(request)
                                      )

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
                return HttpResponseRedirect('/')

    else:
        user = User.objects.get(username=request.user.username)
        try:
            auctionUser = Auction_User.objects.get(user=user)
        except Auction_User.DoesNotExist:
            auctionUser = Auction_User()
        return render_to_response("Users/editAccount.html",
                                  {'myAccountactive':'active','fname':user.first_name,'lname':user.last_name,'username':request.user.username,'email':request.user.email,'address':auctionUser.address,'phone':auctionUser.phone},
                                  context_instance=RequestContext(request)
                                  )