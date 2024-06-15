# Generated by Django 4.2 on 2024-06-15 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0012_topic_alter_challenge_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='challenge.topic', verbose_name='topic'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic',
            field=models.CharField(max_length=255, verbose_name='topic'),
        ),
    ]
