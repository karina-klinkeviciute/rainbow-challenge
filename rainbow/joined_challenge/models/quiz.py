from joined_challenge.models.base import BaseJoinedChallenge


class QuizJoinedChallenge(BaseJoinedChallenge):

    @property
    def concrete_challenge(self):
        from challenge.models import CustomChallenge
        return CustomChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)

    # todo method for returning the quizuser object or other info from that model
