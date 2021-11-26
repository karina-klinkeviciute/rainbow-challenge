import uuid

import isoweek
from django.db import models
from django.utils.translation import gettext_lazy as _


class StreakChangeOptions:
    INCREASED = 1
    DECREASED = -1
    ZERO = 0

    StreakChangeChoices = (
        (INCREASED, _("increased")),
        (DECREASED, _("decreased")),
        (ZERO, _("zero"))
    )


class Streak(models.Model):

    """
    Class for user streaks.
    We create a new object every week that holds information about
    that week and at what level the streak is on that week.
    We could have only one object, holding only the last streak but then we would loose info on how
    it changes overtime.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False)
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name=_("user")
    )
    time_added = models.DateTimeField(
        verbose_name=_("time_added"),
        auto_now_add=True,
    )
    year = models.IntegerField(
        verbose_name=_("year")
    )
    week = models.IntegerField(
        verbose_name=_("week number")
    )
    streaks = models.IntegerField(
        verbose_name=_("streaks in a row")
    )
    change = models.IntegerField(
        choices=StreakChangeOptions.StreakChangeChoices,
        verbose_name=_("change"),
    )

    class Meta:
        unique_together = ('user', 'year', 'week')
