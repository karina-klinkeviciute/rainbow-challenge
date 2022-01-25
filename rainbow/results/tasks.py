from datetime import date
import isoweek

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from django.utils.translation import gettext_lazy as _

from joined_challenge.models import JoinedChallenge
from message.models import Message, MessageTypes
from results.models import Streak, Medal, MedalTypes
from user.models import User


@shared_task
def test_task():
    message = Message(
        message_text="celery works alright",
    )
    message.save()
    send_mail(
        _('Celery works alright'),
        'celery works alright',
        'no-reply@rainbowchallenge.lt',
        settings.ADMIN_EMAILS,
        fail_silently=True,
    )


@shared_task
def calculate_streaks():
    """
    Calculate streaks for all users for the last week.
    To be run weekly with celery crontab.
    """

    # Calculating streaks

    stats = {
        "streaks_increased": 0,
        "streaks_decreased": 0,
        "medals": {level: 0 for level in MedalTypes.MedalLevels.values()}}

    current_week = date.today().isocalendar()[1]

    last_week = current_week - 1
    stats["week"] = last_week
    week_before_last = last_week - 1
    last_weeks_year = week_before_last_year = date.today().year
    if last_week == 0:
        last_weeks_year -= 1
        week_before_last_year -= 1
        last_week = isoweek.Week.last_week_of_year(last_weeks_year)
        week_before_last = isoweek.Week.last_week_of_year(week_before_last_year) - 1
    if week_before_last == 0:
        week_before_last_year -= 1
        week_before_last = isoweek.Week.last_week_of_year(week_before_last_year)

    stats["year"] = last_weeks_year

    for user in User.objects.all():

        # Get latest streak
        try:
            streak = Streak.objects.get(
                user=user,
                week=week_before_last,
                year=week_before_last_year
            )
            streaks = streak.streaks

        except Streak.DoesNotExist:
            streaks = 0

        # calculate last week's change and streak

        if challenges_completed_at_week(user, last_week):
            change = 1
            stats["streaks_increased"] += 1
        else:
            if streaks > 0:
                change = -1
                stats["streaks_decreased"] += 1
            else:
                # if streaks is 0 this means that user has been inactive for some weeks and if we go negative,
                # it might be difficult to climb up again, we don't want that. In other words, we never go below zero.
                change = 0

        streaks += change

        Streak.objects.create(
            user=user,
            week=last_week,
            year=last_weeks_year,
            streaks=streaks,
            change=change
        )

        # check if we need to issue a new medal
        # and issue if needed
        if streaks in MedalTypes.MedalLevels:
            level = MedalTypes.MedalLevels[streaks]
            if not Medal.objects.filter(user=user, level=level).exists():
                Medal.objects.create(user=user, level=level)
                stats["medals"][level] += 1

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

    medals_stats = "".join([f"{v}: {k} " for v, k in stats["medals"].items()])

    email_text = _("""
    Statistics for streaks:
    year: {}
    week:{}
    streaks increased: {}
    streaks decreased: {}
    medals: {}
    
    """).format(stats["year"], stats["week"], stats["streaks_increased"], stats["streaks_decreased"], medals_stats)

    send_mail(
        _('Streaks and medals statistics'),
        email_text,
        'no-reply@rainbowchallenge.lt',
        settings.ADMIN_EMAILS,
        fail_silently=False,
    )


def challenges_completed_at_week(user, week):
    return JoinedChallenge.objects.filter(user=user, completed_at__week=week).count()


