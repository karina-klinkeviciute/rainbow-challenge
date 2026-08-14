"""Smoke test for the Djoser/social-auth provider endpoint.

This is the URL the mobile app opens to start a Google login, and the only
place social-auth's backend machinery runs in-process (everything else in the
login flow talks to Google or Apple over the network). It is worth a test
because it breaks silently on social-auth upgrades.
"""
import pytest

pytestmark = pytest.mark.django_db


def test_google_provider_auth_returns_an_authorization_url(api_client, settings):
    settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "client-id"
    settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "client-secret"

    response = api_client.get(
        "/auth/o/google-oauth2/",
        {"redirect_uri": "https://rainbowchallenge.lt"},
    )

    assert response.status_code == 200
    url = response.data["authorization_url"]
    assert url.startswith("https://accounts.google.com/o/oauth2/auth")
    assert "client_id=client-id" in url
