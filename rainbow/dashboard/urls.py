from django.urls import path, include

from dashboard.views.dashboard import DashboardView
from dashboard.views.confirmation import ConfirmListView, ConfirmDetailView
from dashboard.views.prize import ClaimedPrizeIssueListView, ClaimedPrizeIssueDetailView

urlpatterns = [
    # dashboard
    path('', DashboardView.as_view(), name="dashboard"),
    path('confirmation/', ConfirmListView.as_view(), name="confirmation-list"),
    path('confirmation/<uuid:pk>', ConfirmDetailView.as_view(), name="confirmation-detail"),
    path('prize/', ClaimedPrizeIssueListView.as_view(), name="prize-issue-list"),
    path('prize/<uuid:pk>', ClaimedPrizeIssueDetailView.as_view(), name="prize-issue-detail"),
    ]
