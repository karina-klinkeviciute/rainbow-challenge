from django.views.generic import TemplateView

from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus
from results.models import ClaimedPrize
from user.mixins import StaffRequiredMixin


class DashboardView(StaffRequiredMixin, TemplateView):
    """
    Dashboard view. Links to actions for admins to perform.

    Staff-only: it links to admin actions (e.g. the confirmation list, which is
    itself staff-gated), so a non-admin would only reach dead 403 links.
    """
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Surface how many submissions are waiting so admins see the workload at
        # a glance. Same filter the confirmation list uses (status COMPLETED).
        context["pending_confirmations_count"] = JoinedChallenge.objects.filter(
            status=JoinedChallengeStatus.COMPLETED
        ).count()

        # Prizes users have claimed but that an admin has not handed over yet.
        context["pending_prize_issuance_count"] = ClaimedPrize.objects.filter(
            issued=False
        ).count()

        return context
