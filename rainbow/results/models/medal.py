# We will calcualte weekly streaks on the fly.

# Medals will be calculated each Monday morning and assigned if needed.
# We could add celery and run crontab task each Monday

# Options for calculating streaks:

# 1. We can store them in the database for each week, with references to the completed tasks.
# We could count them together with medals.

# 2. We can calculate them on the fly when the user checks their profile
# We shouldn't calculate them on the fly. Because if user goes to zero, goes like that for a few weeks and then
# does a challenge, they would be still at zero, though they shouldn't, their streak should start again.

# We could take that into account in our formula but maybe having them each week will be more convenient.

# We probably need celery to run every Monday morning and calculate the streaks and the medals.

#  Not sure what to do with challenges if they are completed one week but confirmed another one.
#  Maybe we can count them in and not worry much about confirmation?

# For medals we will have a model where we will store the highest medal achieved.

# We can count how many weeks are since the participant joined and add
# all the weeks with completed tasks and subtract all those without.
# It shouldn't take too long as there are only 52 weeks in the year
# so even after a few years it would be a couple of hundreds of weeks so easy to iterate through
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class MedalTypes:
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"

    MedalChoices = (
        (BRONZE, _("bronze")),
        (SILVER, _("silver")),
        (GOLD, _("gold")),
        (PLATINUM, _("platinum")),
    )

    MedalLevels = {
        BRONZE: 10,
        SILVER: 20,
        GOLD: 30,
        PLATINUM: 40
    }


class Medal(models.Model):
    """Class for medals that users get for doing streaks
        Medals can be only one of each level, we need to take care of that
    """
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name=_("user")
    )
    level = models.CharField(
        choices=MedalTypes.MedalChoices,
        max_length=255,
        verbose_name=_("level")
    )
    time_issued = models.DateTimeField(
        verbose_name=_("time_issued"),
        auto_now_add=True,
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False)

    class Meta:
        unique_together = ('user', 'level')
