# We will calcualte weekly streaks on the fly.

# Medals will be calculated each Monday morning and assigned if needed.
# We could add celery and run crontab task each Monday

# Options for calculating streaks:

# 1. We can store them in the database for each week, with references to the completed tasks.
# We could count them together with medals.

# 2. We can calculate them on the fly when the user checks their profile

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
    """Class for medals that users get for doing streaks"""
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    level = models.CharField(choices=MedalTypes.MedalChoices, max_length=255)
    time = models.DateTimeField()
    uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False)
