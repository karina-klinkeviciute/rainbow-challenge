"""Settings used when running the test suite.

Inherits everything from the production settings (so tests exercise the real
configuration) and only overrides what would make tests slow, flaky, or
dependent on external services:

- ``SECURE_SSL_REDIRECT`` is turned off so the test client's http requests
  reach the views instead of being 301-redirected to https.
- A fast password hasher keeps user-creating tests quick.
- E-mail is sent to an in-memory outbox instead of a real SMTP server
  (djoser sends activation/confirmation e-mails on user creation).
- Celery tasks run eagerly and in-process.

The database stays on PostgreSQL (as in production); Django creates a separate
``test_<name>`` database automatically.
"""
from rainbow_project.settings import *  # noqa
from rainbow_project.settings import REST_FRAMEWORK

SECURE_SSL_REDIRECT = False

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Run Celery tasks synchronously so results are available immediately and no
# broker is required during tests.
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Keep the production permission default (IsAuthenticated) explicit for tests:
# the dev settings drop it, and we want tests to assert the real behaviour.
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
