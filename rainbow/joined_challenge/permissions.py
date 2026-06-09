from rest_framework.permissions import BasePermission, IsAuthenticated


class IsJoinedChallengeOwner(BasePermission):
    """Object-level permission granting access only to a joined challenge's owner.

    The object handed to ``has_object_permission`` is expected to be a (main)
    ``JoinedChallenge``. As with :class:`UserOwnedQuerysetMixin`, cross-user
    access is reserved for the Django admin interface, so this deliberately
    excludes admins -- only the owning user passes.

    Views that don't resolve the object through ``get_object`` (e.g. uploads
    keyed off ``validated_data`` or a concrete uuid) must invoke it explicitly
    via ``self.check_object_permissions(request, joined_challenge)``.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UserOwnedQuerysetMixin:
    """Restrict a viewset/generic view to joined challenges owned by the user.

    Through the API, a user may only access their own joined challenges
    (see issue #104). The requesting user must be authenticated and only ever
    sees objects they own -- this includes admins: cross-user access is
    available solely through the 2FA-protected Django admin interface, not the
    API.

    The lookup connecting an object to its owning user is configured with
    ``owner_lookup_field`` (e.g. ``user`` for ``JoinedChallenge`` or
    ``main_joined_challenge__user`` for the concrete joined challenges).
    """
    permission_classes = [IsAuthenticated]
    owner_lookup_field = 'user'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(**{self.owner_lookup_field: self.request.user})