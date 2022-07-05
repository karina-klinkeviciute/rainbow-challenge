from rest_framework.response import Response
from rest_framework.views import APIView

from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus
from results.models import ClaimedPrize


class BalanceView(APIView):
    """A view for Rainbows earning/spending data"""
    def get(self, request, format=None):
        earning = []
        spending = []
        user = self.request.user
        all_confirmed_challenges = JoinedChallenge.objects.filter(user=user, status=JoinedChallengeStatus.CONFIRMED)
        for confirmed_challenge in all_confirmed_challenges:
            earning.append({
                "name": confirmed_challenge.challenge.name,
                "points": confirmed_challenge.challenge.points
            })

        all_prizes = ClaimedPrize.objects.filter(user=user)

        for prize in all_prizes:
            spending.append({
                "name": prize.prize.name,
                "amount": prize.amount,
                "price": prize.prize.price,
                "total": prize.amount*prize.prize.price
            })

        earned_rainbows = user.all_points
        remaining_rainbows = user.remaining_points

        balance = {
            "earned_rainbows": earned_rainbows,
            "remaining_rainbows": remaining_rainbows,
            "earning": earning,
            "spending": spending
        }

        return Response(balance)
