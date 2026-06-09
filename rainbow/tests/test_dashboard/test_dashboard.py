"""Tests for the dashboard landing view.

The dashboard links to admin-only actions (confirmation, etc.), so it is
staff-gated via the shared StaffRequiredMixin: anonymous users are redirected to
login, authenticated non-admins get a 403, and staff see the page.
"""
import pytest
from django.test import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db


def logged_in_client(user):
    client = Client()
    client.force_login(user)
    return client


def test_dashboard_requires_login():
    response = Client().get(reverse("dashboard"))

    assert response.status_code == 302


def test_dashboard_forbidden_for_non_staff(user):
    response = logged_in_client(user).get(reverse("dashboard"))

    assert response.status_code == 403


def test_dashboard_renders_for_staff(admin_user):
    response = logged_in_client(admin_user).get(reverse("dashboard"))

    assert response.status_code == 200
