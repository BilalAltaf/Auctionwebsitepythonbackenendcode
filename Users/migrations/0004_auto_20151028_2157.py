# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_auto_20151028_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_user',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 57, 54, 253000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction_user',
            name='lastUpdatedDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 57, 54, 253000)),
            preserve_default=True,
        ),
    ]
