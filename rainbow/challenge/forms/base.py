from django import forms

from challenge.models import Challenge


class BaseChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = (
            'name',
            'description',
            'points',
            'region',
            'start_date',
            'end_date',
            'multiple',
            'needs_confirmation',
            'published',
        )
