from challenge.models.challenge.school_gsa import SchoolGSAChallenge
from challenge.models.joined_challenge.base import BaseJoinedChallenge


class SchoolGSAJoinedChallenge(BaseJoinedChallenge):

    @property
    def concrete_challenge(self):
        return SchoolGSAChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
