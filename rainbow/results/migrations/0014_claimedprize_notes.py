# Generated by Django 3.2.16 on 2023-07-11 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0013_auto_20230126_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimedprize',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='notes'),
        ),
    ]