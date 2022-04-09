# Generated by Django 3.2.9 on 2022-04-09 13:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0009_auto_20220409_1341'),
        ('joined_challenge', '0012_auto_20220214_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizjoinedchallenge',
            name='quiz_user',
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenge.answer', verbose_name='answer')),
                ('quiz_joined_challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='joined_challenge.quizjoinedchallenge', verbose_name='quiz joined challenge')),
            ],
        ),
    ]
