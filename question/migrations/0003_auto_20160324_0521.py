# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 23:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20160324_0512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
    ]
