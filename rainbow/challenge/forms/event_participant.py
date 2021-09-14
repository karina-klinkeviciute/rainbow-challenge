from django import forms

from challenge.forms.base import BaseChallengeForm


class EventParticipantChallengeForm(BaseChallengeForm):
    event_name = forms.CharField()
    date = forms.DateField()
    url = forms.URLField()
