"""Shared Django-admin permission mixins.

In this project ``User.has_perm``/``has_module_perms`` return ``True`` for
everyone, so any ``is_admin`` (staff) user otherwise gets full access to every
registered model. These mixins narrow that for sensitive models.
"""


class SuperuserOnlyAdminMixin:
    """Gate a ``ModelAdmin`` behind ``is_superuser``.

    Ordinary admins (``is_admin`` / staff) keep access to the operational models,
    but a ``ModelAdmin`` mixing this in is reachable only by superusers -- used
    for privilege-sensitive or system-configuration data (user accounts, prizes,
    regions/medals/streaks) that regular admins must not view or change.

    Put it first in the base list so its overrides win over Django's defaults,
    e.g. ``class UserAdmin(SuperuserOnlyAdminMixin, BaseUserAdmin)``.
    """

    @staticmethod
    def _is_superuser(request):
        return bool(getattr(request, "user", None) and request.user.is_superuser)

    def has_module_permission(self, request):
        return self._is_superuser(request)

    def has_view_permission(self, request, obj=None):
        return self._is_superuser(request)

    def has_add_permission(self, request):
        return self._is_superuser(request)

    def has_change_permission(self, request, obj=None):
        return self._is_superuser(request)

    def has_delete_permission(self, request, obj=None):
        return self._is_superuser(request)
