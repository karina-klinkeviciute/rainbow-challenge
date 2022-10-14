from django.urls import path, include

from dashboard.views.dashboard import DashboardView
from joined_challenge.views.confirmation import ConfirmListView, ConfirmDetailView

urlpatterns = [
    # dashboard
    path('', DashboardView.as_view(), name="dashboard"),
    path('confirmation/', ConfirmListView.as_view(), name="confirmation"),
    path('confirmation/<uuid>', ConfirmDetailView.as_view(), name="confirmation-detail"),
    ]
