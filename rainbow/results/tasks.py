from celery import shared_task


@shared_task
def calculate_streaks():
    """
    Calculate streaks for all users for the last week.
    To be run weekly with celery crontab.
    """

    # first step - calculate streaks for the last week.

    # second step - check medals and save

    # third - send email about results to info@rainbowchallenge.lt

    # forth - send messages
    # 1. positive messsage to everyone advancing with a streak
    # 2. sorry message to anyone who missed a streak (and got 1-)
    # everyone who got a new medal (10 streaks - bronze, 20 - silver etc)



