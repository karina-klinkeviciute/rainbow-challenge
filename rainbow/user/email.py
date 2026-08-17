"""Djoser account emails, wired up in ``settings.DJOSER['EMAIL']``.

Djoser's email classes keep the originating ``HttpRequest`` on the message
object (they need it to build the domain/protocol context). That reference
outlives the rendering, and an email message that carries a request cannot be
copied or pickled: since Django 5.1 ``ResolverMatch`` refuses to be pickled, so
anything that deep-copies the message — the locmem backend used in tests, or a
queue if these mails are ever handed to Celery — blows up with
``PicklingError: Cannot pickle ResolverMatch``.

Nothing needs the request once the subject and body are rendered, so we drop it
right after.
"""
from djoser import email


class DropRequestAfterRenderMixin:
    """Let go of the request once the message has been rendered."""

    def render(self):
        super().render()
        self.request = None


class ActivationEmail(DropRequestAfterRenderMixin, email.ActivationEmail):
    pass


class ConfirmationEmail(DropRequestAfterRenderMixin, email.ConfirmationEmail):
    pass


class PasswordResetEmail(DropRequestAfterRenderMixin, email.PasswordResetEmail):
    pass


class PasswordChangedConfirmationEmail(
    DropRequestAfterRenderMixin, email.PasswordChangedConfirmationEmail
):
    pass


class UsernameChangedConfirmationEmail(
    DropRequestAfterRenderMixin, email.UsernameChangedConfirmationEmail
):
    pass


class UsernameResetEmail(DropRequestAfterRenderMixin, email.UsernameResetEmail):
    pass
