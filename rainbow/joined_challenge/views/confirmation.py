from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus


class ConfirmListView(LoginRequiredMixin, ListView):
    """Lists all challenges that need confirmation"""
    model = JoinedChallenge
    template_name = "joined_challenge/confirmation_list.html"

    def get_queryset(self):
        return JoinedChallenge.objects.filter(status=JoinedChallengeStatus.COMPLETED)


class ConfirmDetailView(LoginRequiredMixin, DetailView):
    """

    """
    pass
