"""Tests for the django-import-export admin exports.

The association exports users and joined challenges from the admin to work with
the data in a spreadsheet, so both the resources and the spreadsheet formats
they can be exported as are worth guarding — version 4 of the library stopped
pulling the xlsx/ods backends in by default.
"""
import pytest

from import_export.formats.base_formats import CSV, ODS, XLSX

from joined_challenge.admin import JoinedChallengeAdmin, JoinedChallengeResource
from joined_challenge.models import JoinedChallenge
from user.admin import UserAdmin, UserResource
from user.models import User

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("format_class", [CSV, XLSX, ODS])
def test_spreadsheet_export_formats_are_available(format_class):
    assert format_class.is_available()


def test_admins_declare_their_resource():
    # `resource_class` was removed in favour of `resource_classes`; a stale
    # spelling would silently fall back to an auto-generated resource.
    assert JoinedChallengeAdmin.resource_classes == [JoinedChallengeResource]
    assert UserAdmin.resource_classes == [UserResource]


def test_joined_challenge_export_contains_the_challenge_and_user(
    user, make_joined_challenge,
):
    make_joined_challenge(user)

    dataset = JoinedChallengeResource().export(JoinedChallenge.objects.all())

    assert "user__email" in dataset.headers
    assert dataset.dict[0]["user__email"] == user.email


def test_user_export_is_the_anonymised_column_set(make_user):
    make_user(year_of_birth=1999)

    dataset = UserResource().export(User.objects.all())

    # Deliberately no email or name: this export is for demographics.
    assert dataset.headers == [
        "date_joined", "gender", "gender_other", "region__name", "year_of_birth",
    ]
    assert dataset.dict[0]["year_of_birth"] == "1999"
