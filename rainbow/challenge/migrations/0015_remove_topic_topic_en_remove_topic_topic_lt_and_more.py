# Generated by Django 4.2 on 2024-06-15 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0014_topic_topic_en_topic_topic_lt_topic_topic_pt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='topic_en',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='topic_lt',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='topic_pt',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='topic_sk',
        ),
    ]