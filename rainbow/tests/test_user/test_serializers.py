"""Tests for ``user/serializers.py`` - the ``UserSerializer.update`` logic.

``UserSerializer`` is djoser's ``user`` / ``current_user`` serializer (used by
``/auth/users/me/``). Its custom ``update`` does two things:

  - **Region change:** ``region`` is a nested serializer, but a profile update
    only carries the region's ``uuid``; ``update`` resolves that uuid to a real
    ``Region`` and assigns it (the nested payload itself is discarded).
  - **Email change safety:** if the e-mail changes and activation e-mails are
    on, the account is deactivated until re-activated. In practice ``email`` is
    the read-only ``LOGIN_FIELD``, so this branch can't be reached through the
    serializer's normal input - it's covered here by calling ``update``
    directly to document the safety behaviour.

These are unit tests against the serializer; they call ``save()``/``update``
directly so the (annotation-heavy) read representation isn't built.
"""
import pytest
from model_bakery import baker

from results.models.region import Region
from user.serializers import UserSerializer

pytestmark = pytest.mark.django_db


def test_update_resolves_region_from_uuid(user):
    old_region = baker.make(Region, name="Old")
    new_region = baker.make(Region, name="New")
    user.region = old_region
    user.save()

    serializer = UserSerializer(
        instance=user,
        # update() resolves the region from the uuid only; the nested "name"
        # is discarded, so it just needs to pass the serializer's validation
        # (Region.name is unique, hence a fresh value here).
        data={"region": {"uuid": str(new_region.uuid), "name": "Payload name"}},
        partial=True,
    )
    assert serializer.is_valid(), serializer.errors
    serializer.save()

    user.refresh_from_db()
    assert user.region == new_region


def test_update_without_region_leaves_it_unchanged(user):
    region = baker.make(Region, name="Stable")
    user.region = region
    user.save()

    serializer = UserSerializer(
        instance=user, data={"year_of_birth": 1990}, partial=True,
    )
    assert serializer.is_valid(), serializer.errors
    serializer.save()

    user.refresh_from_db()
    assert user.year_of_birth == 1990
    assert user.region == region  # untouched


def test_update_deactivates_account_on_email_change(user):
    # The email-change branch is unreachable via normal input (email is the
    # read-only LOGIN_FIELD), so drive update() directly to document that an
    # email change forces re-activation.
    user.is_active = True
    user.save()

    serializer = UserSerializer(instance=user, data={}, partial=True)
    serializer.update(user, {"email": "changed@example.com"})

    user.refresh_from_db()
    assert user.email == "changed@example.com"
    assert user.is_active is False