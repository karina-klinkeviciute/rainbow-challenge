from datetime import datetime, timedelta

from results.models import Streak


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

#         # check if we need to issue a new medal
#         # and issue if needed
#         if streaks in MedalTypes.MedalLevels:
#             level = MedalTypes.MedalLevels[streaks]
#             if not Medal.objects.filter(user=user, level=level).exists():
#                 Medal.objects.create(user=user, level=level)
#                 stats["medals"][level] += 1
#
#                 # send message about the medal
#                 message_text = _(
#                     "Congratulations! You just reached {} streaks and received a new {} medal!"
#                 ).format(streaks, MedalTypes.MedalNames[level])
#
#                 message = Message(
#                     user=user,
#                     type=MessageTypes.MEDAL,
#                     message_text=message_text
#                 )
#                 message.save()
#
#     medals_stats = "".join([f"{v}: {k} " for v, k in stats["medals"].items()])
#
#     email_text = _("""
#     Statistics for streaks:
#     year: {}
#     week:{}
#     streaks increased: {}
#     streaks decreased: {}
#     medals: {}
#
#     """).format(stats["year"], stats["week"], stats["streaks_increased"], stats["streaks_decreased"], medals_stats)
#
#     send_mail(
#         _('Streaks and medals statistics'),
#         email_text,
#         'rainbowchallenge@rainbowchallenge.lt',
#         settings.ADMIN_EMAILS,
#         fail_silently=False,
#     )
#
# def challenges_completed_at_week(user, week):
#     return JoinedChallenge.objects.filter(user=user, completed_at__week=week).count()


