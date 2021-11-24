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

    """Class for user streaks"""
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

    # @property
    # def change(self):
    #     """
    #     Returns if the streak has increased or decreased or stayed at zero.
    #     """
    #     last_week = self.week - 1
    #     year = self.year
    #     if last_week == 0:
    #         year = year - 1
    #         last_week = isoweek.Week.last_week_of_year(year)
    #
    #     try:
    #         last_streak =
