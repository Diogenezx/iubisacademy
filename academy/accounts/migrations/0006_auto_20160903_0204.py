# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-03 02:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user/profile', verbose_name='Imagem do usuário'),
        ),
    ]
