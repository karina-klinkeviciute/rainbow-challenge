from django.db import models
from django.utils.translation import gettext_lazy as _

from challenge.models.base import BaseChallenge


class CustomChallenge(BaseChallenge):
    """Article challenge"""
    pass
