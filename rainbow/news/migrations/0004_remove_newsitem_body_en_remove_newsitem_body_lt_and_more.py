# Generated by Django 4.2 on 2024-06-15 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_newsitem_body_en_newsitem_body_lt_newsitem_body_pt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsitem',
            name='body_en',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='body_lt',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='body_pt',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='body_sk',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='published_en',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='published_lt',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='published_pt',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='published_sk',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='title_lt',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='title_pt',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='title_sk',
        ),
    ]
