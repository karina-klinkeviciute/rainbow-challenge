from rest_framework.permissions import IsAuthenticated


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