# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0005_auto_20160324_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(default='', max_length=1024),
        ),
    ]
