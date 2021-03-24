import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class GenderOptions:
    """Class for challenge types. Used in choices for Challenge Type"""
    WOMAN = 'woman'
    MAN = 'man'
    NONBINARY = 'non-binary'
    OTHER = 'other'
    PREFERNOT = 'prefer_not_to_say'

    GENDER_CHOICES = (
        (WOMAN, _('woman')),
        (MAN, _('man')),
        (NONBINARY, _('non-binary')),
        (OTHER, _('other')),
        (PREFERNOT, _('prefer not to say')),
    )


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        null=True,
    )
    email = models.EmailField(_('email address'), blank=True, unique=True)
    year_of_birth = models.IntegerField(verbose_name=_('year of birth'))
    gender = models.CharField(
        verbose_name=_('gender'),
        choices=GenderOptions.GENDER_CHOICES,
        max_length=255,
        blank=True,
        null=True
    )
    gender_other = models.CharField(
        verbose_name=_("enter gender if selected other"),
        max_length=255,
        blank=True,
        null=True
    )
    region = models.ForeignKey(
        'challenge.Region',
        verbose_name=_('region'),
        on_delete=models.SET_NULL,
        null=True
    )
    is_active = models.BooleanField(_('is active'), default=True)
    is_admin = models.BooleanField(_('is admin'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['year_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
