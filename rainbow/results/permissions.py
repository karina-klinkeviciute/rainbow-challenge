from rest_framework.permissions import BasePermission


class IsClaimedPrizeOwner(BasePermission):
    """Object-level permission granting access only to a claimed prize's owner.

    Mirrors ``joined_challenge.permissions.IsJoinedChallengeOwner``: through the
    API a user may only reach their own points/prizes data, and cross-user access
    is reserved for the 2FA-protected Django admin interface -- so this
    deliberately excludes admins too, only the owning user passes.

    ``ClaimedPrizeViewSet`` already scopes its queryset to the requesting user, so
    this is defence-in-depth: it keeps the ownership rule explicit and returns a
    clear 403 (rather than relying solely on a 404 from the filtered queryset)
    should a future change widen that queryset.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
