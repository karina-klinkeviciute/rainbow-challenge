# Generated by Django 3.2.9 on 2021-12-18 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joined_challenge', '0009_auto_20211214_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlejoinedchallenge',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
    ]