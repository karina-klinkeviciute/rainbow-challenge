from django.db import models
from django.utils.translation import gettext_lazy as _
from protected_media.models import ProtectedFileField

from joined_challenge.models import JoinedChallenge


class Attachment(models.Model):
    """
    A class for a attached file
    """
    file = ProtectedFileField(upload_to="uploads/")
    joined_challenge = models.ForeignKey(JoinedChallenge, on_delete=models.SET_NULL)


class TestAttachment(models.Model):
    """
    A class only for testing the uploads and viewing only for protected files
    """
    file = ProtectedFileField(upload_to="uploads/")
