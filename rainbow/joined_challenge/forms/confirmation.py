from django import forms


class ConfirmationForm(forms.Form):
    joined_challenge_uuid = forms.UUIDField()

