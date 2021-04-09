# Generated by Django 3.1.6 on 2021-04-09 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('challenge', '0007_prize_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaimedPrize',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.IntegerField(verbose_name='amount')),
                ('issued', models.BooleanField(default=False, verbose_name='issued')),
                ('prize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenge.prize', verbose_name='prize')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]