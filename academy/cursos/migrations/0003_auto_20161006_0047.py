# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-06 00:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0002_auto_20161006_0006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='Autor',
        ),
        migrations.AddField(
            model_name='curso',
            name='autor',
            field=models.CharField(default=1, max_length=20, verbose_name='Autor'),
            preserve_default=False,
        ),
    ]