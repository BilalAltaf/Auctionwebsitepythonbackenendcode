# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AuctionApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('itemDescription', models.CharField(max_length=300)),
                ('minPrice', models.FloatField(default=0)),
                ('topBid', models.FloatField(default=0)),
                ('topBidNo', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=1)),
                ('winner', models.CharField(default=b'', max_length=30)),
                ('deadline', models.DateTimeField(default=datetime.datetime(2015, 10, 28, 19, 32, 1, 509000))),
                ('createdDate', models.DateTimeField(default=datetime.datetime(2015, 10, 28, 19, 32, 1, 509000))),
                ('lastModifiedDate', models.DateTimeField(default=datetime.datetime(2015, 10, 28, 19, 32, 1, 509000))),
                ('category', models.ForeignKey(to='AuctionApp.itemType')),
                ('seller', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Auction_Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField(default=0)),
                ('bidNumber', models.IntegerField(default=0)),
                ('comment', models.CharField(max_length=300)),
                ('bidDate', models.DateTimeField(default=datetime.datetime(2015, 10, 28, 19, 32, 1, 512000))),
                ('auction', models.ForeignKey(to='Auctions.Auction')),
                ('bidUser', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
