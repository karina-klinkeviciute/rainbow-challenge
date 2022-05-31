import json
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser

from challenge.models import Challenge
from challenge.models.base import ChallengeType
from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus
from results.models import Streak
from results.models.region import Region


class UserManager(BaseUserManager):
    def create_user(self, email, year_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            year_of_birth=year_of_birth,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, year_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            year_of_birth=year_of_birth,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class GenderOptions:
    """Class for question options"""
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
    genders = {gender[0]: gender[1] for gender in GENDER_CHOICES}


class IsLGBTQIAOptions:
    """Class for question options types"""
    YES = 'yes'
    NO = 'no'
    PREFERNOT = 'prefer_not_to_say'

    IsLGBTQIA_CHOICES = (
        (YES, _('yes')),  # temporary until translation is ready
        (NO, _('no')),
        (PREFERNOT, _('prefer not to say')),
    )

    def __init__(self):
        options = dict()
        for option in self.IsLGBTQIA_CHOICES:
            options[option[0]] = option[1]
        self.options = options


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    uid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
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
    year_of_birth = models.IntegerField(
        verbose_name=_('year of birth'),
        blank=True,
        null=True
    )
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
        Region,
        verbose_name=_('region'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_lgbtqia = models.CharField(
        choices=IsLGBTQIAOptions.IsLGBTQIA_CHOICES,
        verbose_name=_('Do you consider yourself LGBTQIA+?'),
        null=True,
        blank=True,
        max_length=255
    )
    is_active = models.BooleanField(_('is active'), default=False)
    is_admin = models.BooleanField(_('is admin'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['year_of_birth', ]
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def completed_joined_challenges(self):
        return self.joinedchallenge_set.filter(status=JoinedChallengeStatus.COMPLETED)

    @property
    def confirmed_joined_challenges(self):
        return self.joinedchallenge_set.filter(status=JoinedChallengeStatus.CONFIRMED)

    @property
    def completed_challenges(self):
        return Challenge.objects.filter(
            joinedchallenge__user=self,
            joinedchallenge__status=JoinedChallengeStatus.COMPLETED)

    @property
    def confirmed_challenges(self):
        return Challenge.objects.filter(
            joinedchallenge__user=self,
            joinedchallenge__status=JoinedChallengeStatus.CONFIRMED)

    @property
    def quiz_points(self):
        all_joined_challenges = self.joinedchallenge_set
        quiz_joined_challenges = all_joined_challenges.filter(
            challenge__type=ChallengeType.QUIZ,
            status=JoinedChallengeStatus.CONFIRMED
        )
        points = 0
        for quiz_joined_challenge in quiz_joined_challenges:
            points += quiz_joined_challenge.quizjoinedchallenge.correct_answers_count
        return points

    # TODO fix this to reflect changes in the quiz model

    @property
    def all_points(self):
        sum_all = self.confirmed_challenges.aggregate((Sum('points')))
        sum_field = sum_all.get('points__sum')
        if sum_field is None:
            sum_field = 0
        points = sum_field + self.quiz_points
        return points

    @property
    def remaining_points(self):
        claimed_prizes = self.claimedprize_set.all()
        points_used = 0
        for claimed_prize in claimed_prizes:
            points_used += claimed_prize.amount * claimed_prize.prize.price
        return self.all_points - points_used

    @property
    def claimed_prizes(self):
        """All prizes the user has claimed"""
        return self.claimedprize_set.all()

    @property
    def medals_all(self):
        """property to return a list of medals in a convenient enough format for admin"""
        all_medals = list()
        for medal in self.medal_set.all():
            all_medals.append({'level': medal.level, "time_issued": str(medal.time_issued)})

        return json.dumps(all_medals)

    @property
    def streak(self):
        try:
            latest_streak = self.streak_set.latest('time_added')

            return {"streak": latest_streak.streaks, "change": latest_streak.change}
        except Streak.DoesNotExist:
            return None

    @property
    def medals(self):
        return self.medal_set
