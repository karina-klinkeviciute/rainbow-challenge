# Generated by Django 3.2.9 on 2021-12-07 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0008_streak'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
