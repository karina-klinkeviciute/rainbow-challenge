from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restrict a class-based view to staff (admin) users.

    Some dashboard actions (e.g. confirming a challenge, which awards points)
    must not be available to every logged-in user. Anonymous users are
    redirected to login (by ``LoginRequiredMixin``, which precedes
    ``UserPassesTestMixin`` in the MRO so ``test_func`` never runs for them);
    authenticated non-admins get a 403.

    In this project ``User.is_staff`` is a property returning ``is_admin``, so
    "staff" and "admin" are the same role.
    """

    def test_func(self):
        return self.request.user.is_admin
