# Generated by Django 3.2.9 on 2021-11-26 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('medal', 'medal')], max_length=255, null=True, verbose_name='type')),
                ('automated', models.BooleanField(default=True, verbose_name='automated')),
                ('time_sent', models.DateTimeField(auto_now_add=True, verbose_name='time of sending')),
                ('seen', models.BooleanField(default=False, verbose_name='seen')),
            ],
        ),
    ]
