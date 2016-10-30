# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction_User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('createdDate', models.DateTimeField(default=datetime.datetime(2015, 10, 28, 19, 32, 1, 514000))),
                ('lastUpdatedDate', models.DateTimeField(default=datetime.datetime(2015, 10, 28, 19, 32, 1, 514000))),
                ('defaultLang', models.CharField(default=b'en', max_length=2)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
