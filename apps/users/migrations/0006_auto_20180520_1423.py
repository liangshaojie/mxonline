# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-20 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180520_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '\u6ce8\u518c\u8d26\u53f7'), ('forget', '\u627e\u56de\u5bc6\u7801'), ('updateEmail', '\u4fee\u6539\u90ae\u7bb1')], max_length=8, verbose_name='\u7c7b\u578b'),
        ),
    ]
