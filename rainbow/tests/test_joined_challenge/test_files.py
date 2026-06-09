"""Tests for the joined-challenge file API (upload / list).

Users attach files (proof of completion) to their joined challenges. Files are
stored with django-private-storage; ``PRIVATE_STORAGE_ROOT`` is pointed at a
tmp dir per test so nothing is written into the repo.

Endpoints exercised:
  - POST /api/joined_challenge_file_upload/                 (main joined challenge uuid)
  - GET  /api/joined_challenge_file_list/<uuid>/            (own files only)
  - GET  /api/concrete_joined_challenge_file_list/<type>/<uuid>/
  - POST /api/concrete_joined_challenge_file_upload/        (concrete joined challenge uuid)
"""
from uuid import uuid4

import pytest
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from model_bakery import baker

from challenge.models.base import ChallengeType
from joined_challenge.models import ArticleJoinedChallenge
from joined_challenge.models.base import JoinedChallengeFile
from joined_challenge.views.files import JoinedChallengeFileDetailView

pytestmark = pytest.mark.django_db

UPLOAD_URL = "/api/joined_challenge_file_upload/"
CONCRETE_UPLOAD_URL = "/api/concrete_joined_challenge_file_upload/"


@pytest.fixture
def private_storage_tmp(settings, tmp_path):
    """Keep uploaded files out of the repo by storing them under tmp_path."""
    settings.PRIVATE_STORAGE_ROOT = str(tmp_path)
    return tmp_path


def attach_file(joined_challenge, name="proof.txt", content=b"data"):
    """Create a JoinedChallengeFile with a real (tiny) stored file."""
    jcf = JoinedChallengeFile(joined_challenge=joined_challenge)
    jcf.file.save(name, ContentFile(content), save=True)
    return jcf


# --- upload ---------------------------------------------------------------

def test_upload_file_to_joined_challenge(
    user, auth_client, make_joined_challenge, private_storage_tmp,
):
    joined = make_joined_challenge(user)
    upload = SimpleUploadedFile("proof.txt", b"hello", content_type="text/plain")

    response = auth_client(user).post(
        UPLOAD_URL,
        {"joined_challenge": str(joined.uuid), "file": upload},
        format="multipart",
        secure=True,
    )

    assert response.status_code == 201
    assert JoinedChallengeFile.objects.filter(joined_challenge=joined).count() == 1


def test_upload_requires_authentication(
    api_client, user, make_joined_challenge, private_storage_tmp,
):
    joined = make_joined_challenge(user)
    upload = SimpleUploadedFile("proof.txt", b"hello", content_type="text/plain")

    response = api_client.post(
        UPLOAD_URL,
        {"joined_challenge": str(joined.uuid), "file": upload},
        format="multipart",
        secure=True,
    )

    assert response.status_code in (401, 403)


def test_cannot_upload_to_another_users_joined_challenge(
    user, other_user, auth_client, make_joined_challenge, private_storage_tmp,
):
    theirs = make_joined_challenge(other_user)
    upload = SimpleUploadedFile("proof.txt", b"hello", content_type="text/plain")

    response = auth_client(user).post(
        UPLOAD_URL,
        {"joined_challenge": str(theirs.uuid), "file": upload},
        format="multipart",
        secure=True,
    )

    assert response.status_code == 403
    assert not JoinedChallengeFile.objects.filter(joined_challenge=theirs).exists()


def test_upload_via_concrete_joined_challenge(
    user, auth_client, make_joined_challenge, private_storage_tmp,
):
    joined = make_joined_challenge(user, type=ChallengeType.ARTICLE)
    article = baker.make(ArticleJoinedChallenge, main_joined_challenge=joined)
    upload = SimpleUploadedFile("proof.txt", b"hello", content_type="text/plain")

    response = auth_client(user).post(
        CONCRETE_UPLOAD_URL,
        {
            "challenge_type": ChallengeType.ARTICLE,
            "concrete_joined_challenge_uuid": str(article.uuid),
            "file": upload,
        },
        format="multipart",
        secure=True,
    )

    assert response.status_code == 201
    # The file is attached to the *main* joined challenge, resolved from the
    # concrete one.
    assert JoinedChallengeFile.objects.filter(joined_challenge=joined).count() == 1


def test_cannot_upload_via_concrete_to_another_users_challenge(
    user, other_user, auth_client, make_joined_challenge, private_storage_tmp,
):
    joined = make_joined_challenge(other_user, type=ChallengeType.ARTICLE)
    article = baker.make(ArticleJoinedChallenge, main_joined_challenge=joined)
    upload = SimpleUploadedFile("proof.txt", b"hello", content_type="text/plain")

    response = auth_client(user).post(
        CONCRETE_UPLOAD_URL,
        {
            "challenge_type": ChallengeType.ARTICLE,
            "concrete_joined_challenge_uuid": str(article.uuid),
            "file": upload,
        },
        format="multipart",
        secure=True,
    )

    assert response.status_code == 403
    assert not JoinedChallengeFile.objects.filter(joined_challenge=joined).exists()


def test_concrete_upload_unknown_challenge_type_is_400(user, auth_client):
    upload = SimpleUploadedFile("proof.txt", b"hello", content_type="text/plain")

    response = auth_client(user).post(
        CONCRETE_UPLOAD_URL,
        {
            "challenge_type": "not_a_real_type",
            "concrete_joined_challenge_uuid": str(uuid4()),
            "file": upload,
        },
        format="multipart",
        secure=True,
    )

    # An unknown challenge_type is a bad request param, not a server error.
    assert response.status_code == 400


def test_concrete_upload_missing_concrete_challenge_is_404(user, auth_client):
    upload = SimpleUploadedFile("proof.txt", b"hello", content_type="text/plain")

    response = auth_client(user).post(
        CONCRETE_UPLOAD_URL,
        {
            "challenge_type": ChallengeType.ARTICLE,
            "concrete_joined_challenge_uuid": str(uuid4()),  # does not exist
            "file": upload,
        },
        format="multipart",
        secure=True,
    )

    assert response.status_code == 404


def test_concrete_upload_without_main_joined_challenge_is_404(
    user, auth_client, private_storage_tmp,
):
    # A concrete joined challenge whose main link is unset (the FK is nullable).
    orphan = baker.make(ArticleJoinedChallenge, main_joined_challenge=None)
    upload = SimpleUploadedFile("proof.txt", b"hello", content_type="text/plain")

    response = auth_client(user).post(
        CONCRETE_UPLOAD_URL,
        {
            "challenge_type": ChallengeType.ARTICLE,
            "concrete_joined_challenge_uuid": str(orphan.uuid),
            "file": upload,
        },
        format="multipart",
        secure=True,
    )

    assert response.status_code == 404


# --- list (main joined challenge) -----------------------------------------

def test_file_list_returns_own_files(
    user, auth_client, make_joined_challenge, private_storage_tmp,
):
    joined = make_joined_challenge(user)
    attach_file(joined, name="proof.txt")

    response = auth_client(user).get(
        f"/api/joined_challenge_file_list/{joined.uuid}/", secure=True,
    )

    assert response.status_code == 200
    names = [f["file_name"] for f in response.data["files"]]
    # file_name is the basename, stripped of the upload sub-folder path.
    assert names == ["proof.txt"]


def test_file_list_hides_other_users_joined_challenge(
    user, other_user, auth_client, make_joined_challenge, private_storage_tmp,
):
    theirs = make_joined_challenge(other_user)
    attach_file(theirs)

    response = auth_client(user).get(
        f"/api/joined_challenge_file_list/{theirs.uuid}/", secure=True,
    )

    # The list view's queryset is scoped to request.user, so another user's
    # joined challenge is simply not found.
    assert response.status_code == 404


# --- list (concrete joined challenge) -------------------------------------

def test_concrete_file_list_returns_owner_files(
    user, auth_client, make_joined_challenge, private_storage_tmp,
):
    joined = make_joined_challenge(user, type=ChallengeType.ARTICLE)
    article = baker.make(ArticleJoinedChallenge, main_joined_challenge=joined)
    attach_file(joined, name="proof.txt")

    response = auth_client(user).get(
        f"/api/concrete_joined_challenge_file_list/{ChallengeType.ARTICLE}/{article.uuid}/",
        secure=True,
    )

    assert response.status_code == 200
    assert [f["file_name"] for f in response.data] == ["proof.txt"]


def test_concrete_file_list_forbidden_for_non_owner(
    user, other_user, auth_client, make_joined_challenge, private_storage_tmp,
):
    joined = make_joined_challenge(other_user, type=ChallengeType.ARTICLE)
    article = baker.make(ArticleJoinedChallenge, main_joined_challenge=joined)
    attach_file(joined)

    response = auth_client(user).get(
        f"/api/concrete_joined_challenge_file_list/{ChallengeType.ARTICLE}/{article.uuid}/",
        secure=True,
    )

    assert response.status_code == 403


# --- download access control ----------------------------------------------

def _can_access(file_obj, as_user):
    """Drive JoinedChallengeFileDetailView.can_access_file as a given user."""
    view = JoinedChallengeFileDetailView()
    view.request = RequestFactory().get("/")
    view.request.user = as_user
    private_file = type("PrivateFile", (), {"parent_object": file_obj})()
    return view.can_access_file(private_file)


def test_owner_and_admin_can_download_file_others_cannot(
    user, other_user, admin_user, make_joined_challenge, private_storage_tmp,
):
    joined = make_joined_challenge(user)
    jcf = attach_file(joined)

    assert _can_access(jcf, user) is True          # the owner
    assert _can_access(jcf, admin_user) is True     # an admin
    assert _can_access(jcf, other_user) is False    # an unrelated user


def test_file_detail_lookup_is_by_stored_path(
    user, make_joined_challenge, private_storage_tmp,
):
    joined = make_joined_challenge(user)
    jcf = attach_file(joined, name="proof.txt")

    view = JoinedChallengeFileDetailView()
    view.kwargs = {"path": str(jcf.file)}

    assert view.get_object() == jcf