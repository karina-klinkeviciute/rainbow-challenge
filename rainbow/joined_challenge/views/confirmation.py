from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView

from joined_challenge.forms.confirmation import ConfirmationForm
from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus


class ConfirmListView(LoginRequiredMixin, ListView):
    """Lists all challenges that need confirmation"""
    model = JoinedChallenge
    template_name = "joined_challenge/confirmation_list.html"

    def get_queryset(self):
        return JoinedChallenge.objects.filter(status=JoinedChallengeStatus.COMPLETED)


class ConfirmDetailView(LoginRequiredMixin, DetailView, FormView):
    """
        View for confirmation of chalenge.
    """
    model = JoinedChallenge
    template_name = "joined_challenge/confirmation_detail.html"
    form_class = ConfirmationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        """ method to get confirmation data - basically the id of the joined challenge to confirm"""
        joined_challenge_uuid = kwargs["pk"]
        joined_challenge = JoinedChallenge.objects.get(uuid=joined_challenge_uuid)
        joined_challenge.status = JoinedChallengeStatus.CONFIRMED
        joined_challenge.save()

        return HttpResponseRedirect(reverse('confirmation-list'))
