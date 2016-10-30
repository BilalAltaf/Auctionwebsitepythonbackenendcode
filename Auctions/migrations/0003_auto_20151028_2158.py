# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Auctions', '0002_auto_20151028_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 58, 0, 932000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 58, 0, 931000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction',
            name='lastModifiedDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 58, 0, 932000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction_bid',
            name='bidDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 58, 0, 933000)),
            preserve_default=True,
        ),
    ]
