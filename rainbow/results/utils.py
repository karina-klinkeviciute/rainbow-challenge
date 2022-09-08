from datetime import datetime, timedelta

from django.utils.translation import gettext_lazy as _

from challenge.models.base import ChallengeType
from message.models import Message, MessageTypes
from results.models import Streak, MedalTypes, Medal


def update_streak(user):
    """
    Update streak for user for current week if not updated yet.
    """

    # Calculating streaks

    # Calculating for the Monday of current week, so that the weeks wouldn't break on the change of the year.
    now = datetime.now()
    monday = now - timedelta(days = now.weekday())
    current_week = monday.isocalendar()[1]
    current_year = monday.year

    if not Streak.objects.filter(user=user, week=current_week, year=current_year).exists():

        try:
            latest_streak = Streak.objects.filter(user=user).latest('time_added')
            streaks = latest_streak.streaks + 1
        except Streak.DoesNotExist:
            streaks = 1
        Streak.objects.create(user=user, week=current_week, year=current_year, change=1, streaks=streaks)

        # check if we need to issue a new medal
        # and issue if needed
        if streaks in MedalTypes.MedalLevels:
            level = MedalTypes.MedalLevels[streaks]
            if not Medal.objects.filter(user=user, level=level).exists():
                Medal.objects.create(user=user, level=level)

                # send message about the medal
                message_text = _(
                    "Congratulations! You just reached {} streaks and received a new {} medal!"
                ).format(streaks, MedalTypes.MedalNames[level])

                message = Message(
                    user=user,
                    type=MessageTypes.MEDAL,
                    message_text=message_text
                )
                message.save()
