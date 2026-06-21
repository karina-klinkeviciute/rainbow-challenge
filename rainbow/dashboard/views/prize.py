from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from results.models import ClaimedPrize
from user.mixins import StaffRequiredMixin


class ClaimedPrizeIssueListView(StaffRequiredMixin, ListView):
    """Lists prizes that users have claimed but that have not been issued yet."""
    model = ClaimedPrize
    template_name = "dashboard/claimed_prize_issue_list.html"

    def get_queryset(self):
        # Oldest claims first so the queue is worked through fairly (FIFO).
        return ClaimedPrize.objects.filter(issued=False).order_by("date_claimed")


class ClaimedPrizeIssueDetailView(StaffRequiredMixin, DetailView):
    """
    Review a single claimed prize and act on it.

    Issuing a prize is a two-stage process. An admin can edit a free-text admin
    note and **Save** it (e.g. "reached out to the user", "prize sent") without
    marking the prize issued - the claim stays pending. Only once the user
    confirms they received the prize does the admin **Mark as issued**.
    """
    model = ClaimedPrize
    template_name = "dashboard/claimed_prize_issue_detail.html"

    def post(self, request, *args, **kwargs):
        claimed_prize = self.get_object()
        notes = request.POST.get("notes", claimed_prize.notes)

        if request.POST.get("action") == "issue" and not claimed_prize.issued:
            # Flipping ``issued`` stamps ``date_issued`` in the model's save();
            # because ``issued`` is True the save() does not re-notify admins.
            claimed_prize.notes = notes
            claimed_prize.issued = True
            claimed_prize.save()
            return HttpResponseRedirect(reverse("prize-issue-list"))

        # Note-only save: the claim stays pending so the admin can keep updating
        # it until the prize is handed over. We use a queryset .update() to skip
        # ClaimedPrize.save(), which would otherwise re-send the "please issue
        # this prize" message to admins on every note edit.
        ClaimedPrize.objects.filter(pk=claimed_prize.pk).update(notes=notes)
        return HttpResponseRedirect(
            reverse("prize-issue-detail", kwargs={"pk": claimed_prize.pk})
        )