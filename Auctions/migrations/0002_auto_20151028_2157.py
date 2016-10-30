# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 57, 27, 299000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 57, 27, 299000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction',
            name='lastModifiedDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 57, 27, 299000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction_bid',
            name='bidDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 57, 27, 300000)),
            preserve_default=True,
        ),
    ]
