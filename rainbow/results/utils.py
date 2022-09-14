from django.core.mail import send_mail


def message_site_admins(subject: str, message: str):
    """
    Messages users that have status as admin.
    """
    from user.models import User
    admins = User.objects.filter(is_admin=True).values_list("email", flat=True)
    send_mail(subject,
              message,
              'rainbowchallenge@rainbowchallenge.lt',
              admins,
              fail_silently=True,
        )
