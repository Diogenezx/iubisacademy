# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-06 00:06
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='autor',
        ),
        migrations.AddField(
            model_name='curso',
            name='Autor',
            field=models.CharField(default=1, max_length=20, verbose_name=django.contrib.auth.models.User),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='curso',
            name='categoria',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='categories_tags', to='cursos.Categoria'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='curso',
            name='description',
            field=models.TextField(verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Título'),
        ),
    ]