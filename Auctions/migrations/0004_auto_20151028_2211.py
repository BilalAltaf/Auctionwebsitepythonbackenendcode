# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Auctions', '0003_auto_20151028_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 22, 11, 45, 733000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 22, 11, 45, 733000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction',
            name='lastModifiedDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 22, 11, 45, 734000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction_bid',
            name='bidDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 22, 11, 45, 736000)),
            preserve_default=True,
        ),
    ]
