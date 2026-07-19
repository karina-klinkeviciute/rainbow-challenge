"""Django-admin permission tests.

Sensitive models are restricted to superusers via ``SuperuserOnlyAdminMixin``;
ordinary admins (``is_admin`` / staff) keep access to operational models.
Cross-user access to users' own objects stays out of the API (issue #104) -- see
tests/test_joined_challenge/test_permissions.py and tests/api/test_results_api.py.
"""
import pytest
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

from message.admin import MessageAdmin
from message.models import Message
from results.admin import (
    ClaimedPrizeAdmin,
    MedalAdmin,
    PrizeAdmin,
    RegionAdmin,
    StreakAdmin,
)
from results.models import Medal, Streak
from results.models.prize import ClaimedPrize, Prize
from results.models.region import Region
from user.admin import UserAdmin
from user.models import User

pytestmark = pytest.mark.django_db


SUPERUSER_ONLY = [
    (UserAdmin, User),
    (PrizeAdmin, Prize),
    (ClaimedPrizeAdmin, ClaimedPrize),
    (RegionAdmin, Region),
    (MedalAdmin, Medal),
    (StreakAdmin, Streak),
]

PERMISSION_METHODS = (
    'has_module_permission',
    'has_view_permission',
    'has_add_permission',
    'has_change_permission',
    'has_delete_permission',
)


@pytest.fixture
def superuser(make_user):
    return make_user(is_admin=True, is_superuser=True, is_active=True)


def _request(user):
    request = RequestFactory().get('/admin/')
    request.user = user
    return request


@pytest.mark.parametrize('admin_cls,model', SUPERUSER_ONLY)
@pytest.mark.parametrize('method', PERMISSION_METHODS)
def test_superuser_only_admin_blocks_regular_admin(admin_cls, model, method, admin_user):
    # admin_user is is_admin (staff) but NOT is_superuser.
    model_admin = admin_cls(model, AdminSite())
    assert getattr(model_admin, method)(_request(admin_user)) is False


@pytest.mark.parametrize('admin_cls,model', SUPERUSER_ONLY)
@pytest.mark.parametrize('method', PERMISSION_METHODS)
def test_superuser_only_admin_allows_superuser(admin_cls, model, method, superuser):
    model_admin = admin_cls(model, AdminSite())
    assert getattr(model_admin, method)(_request(superuser)) is True


def test_regular_admin_still_reaches_unrestricted_models(admin_user):
    # Operational models (not mixed with SuperuserOnlyAdminMixin) remain open to
    # ordinary admins, since User.has_perm returns True for everyone.
    model_admin = MessageAdmin(Message, AdminSite())
    request = _request(admin_user)
    assert model_admin.has_module_permission(request) is True
    assert model_admin.has_view_permission(request) is True
    assert model_admin.has_change_permission(request) is True
