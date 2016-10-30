"""Web_ProjectApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'AuctionApp.views.show_index'),
    url(r'^generateData/$', 'AuctionApp.views.create_data'),

    url(r'^register/$', 'Users.views.register_user'),
    url(r'^login/$', 'Users.views.login_user'),
    url(r'^myaccount/$', 'Users.views.edit_account'),

    url(r'^myauctions/$', 'Auctions.views.show_listing'),
    url(r'^createauction/$', 'Auctions.views.create_auction'),
    url(r'^editauction/(?P<auctionId>\d+)/$', 'Auctions.views.edit_auction'),
    url(r'^confirmauction/$', 'Auctions.views.confirm_auction'),
    url(r'^viewauction/(?P<auctionId>\d+)/$', 'Auctions.views.view_auction'),
    url(r'^allauctions/$', 'Auctions.views.show_allAuctions'),
    url(r'^allauctions/(?P<catId>\d+)/$', 'Auctions.views.show_allAuctions'),
    url(r'^bidauction/(?P<auctionId>\d+)/$', 'Auctions.views.bid_auction'),
    url(r'^confirmbid/$', 'Auctions.views.confirm_bid'),
    url(r'^banauction/(?P<auctionId>\d+)/$', 'Auctions.views.ban_auction'),

    url(r'^setlang/$', 'AuctionApp.views.set_lang'),

    url(r'^api/allauctions/$', 'API.views.allAuctions'),
    url(r'^api/viewauctions/(?P<auctionId>\d+)/$', 'API.views.viewauctions'),
    url(r'^api/bidauctions/(?P<auctionId>\d+)/$', 'API.views.bidauctions'),

    url(r'^api/auctionsByCat/(?P<categoryId>\d+)/$', 'API.views.getAuctionsByCat'),
    url(r'^api/registerUser/$', 'API.views.registerUser'),
    url(r'^api/getMyAuctions/$', 'API.views.getMyAuctions'),
    url(r'^api/loginUser/$', 'API.views.loginUser'),
    url(r'^api/editUser/$', 'API.views.editUser'),
    url(r'^api/allCategories/$', 'API.views.allCategories'),
    url(r'^api/getUser/(?P<userId>\d+)/$', 'API.views.getUser'),
    url(r'^api/CreateAuction/$', 'API.views.createAuction'),
    url(r'^api/editAuction/(?P<auctionId>\d+)/$', 'API.views.editAuction'),
    url(r'^api/banAuction/(?P<auctionId>\d+)/$', 'API.views.banAuction'),

)