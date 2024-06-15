# Generated by Django 4.2 on 2024-06-15 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0018_topic_topic_en_topic_topic_lt_topic_topic_pt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='_name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='_name_lt',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='_name_pt',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='_name_sk',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='description_en',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='description_lt',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='description_pt',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='description_sk',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='published_en',
            field=models.BooleanField(default=False, verbose_name='is published'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='published_lt',
            field=models.BooleanField(default=False, verbose_name='is published'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='published_pt',
            field=models.BooleanField(default=False, verbose_name='is published'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='published_sk',
            field=models.BooleanField(default=False, verbose_name='is published'),
        ),
        migrations.AddField(
            model_name='eventparticipantchallenge',
            name='event_name_en',
            field=models.CharField(max_length=1000, null=True, verbose_name='event name'),
        ),
        migrations.AddField(
            model_name='eventparticipantchallenge',
            name='event_name_lt',
            field=models.CharField(max_length=1000, null=True, verbose_name='event name'),
        ),
        migrations.AddField(
            model_name='eventparticipantchallenge',
            name='event_name_pt',
            field=models.CharField(max_length=1000, null=True, verbose_name='event name'),
        ),
        migrations.AddField(
            model_name='eventparticipantchallenge',
            name='event_name_sk',
            field=models.CharField(max_length=1000, null=True, verbose_name='event name'),
        ),
        migrations.AddField(
            model_name='supportchallenge',
            name='organization_en',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='organization'),
        ),
        migrations.AddField(
            model_name='supportchallenge',
            name='organization_lt',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='organization'),
        ),
        migrations.AddField(
            model_name='supportchallenge',
            name='organization_pt',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='organization'),
        ),
        migrations.AddField(
            model_name='supportchallenge',
            name='organization_sk',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='organization'),
        ),
    ]
