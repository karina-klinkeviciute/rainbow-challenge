from datetime import date
import isoweek

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from django.utils.translation import gettext_lazy as _

from joined_challenge.models import JoinedChallenge
from message.models import Message, MessageTypes
from results.models import Streak, Medal, MedalTypes
from user.models import User


# @shared_task
# def test_task():
#     message = Message(
#         message_text="celery works alright",
#     )
#     message.save()
#     send_mail(
#         _('Celery works alright'),
#         'celery works alright',
#         'rainbowchallenge@rainbowchallenge.lt',
#         settings.ADMIN_EMAILS,
#         fail_silently=True,
#     )