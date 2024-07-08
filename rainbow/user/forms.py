from django import forms

class AccountDeletionForm(forms.Form):
    email = forms.EmailField()

