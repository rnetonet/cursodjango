# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-26 12:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Biblioteca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Biblioteca',
                'verbose_name_plural': 'Bibliotecas',
            },
        ),
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Campus',
                'verbose_name_plural': 'Campi',
            },
        ),
        migrations.AddField(
            model_name='biblioteca',
            name='campus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.Campus', verbose_name='Campus'),
        ),
    ]
