# Generated by Django 4.1 on 2022-09-08 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0010_prize_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streak',
            name='streaks',
            field=models.IntegerField(verbose_name='streaks completed'),
        ),
    ]
