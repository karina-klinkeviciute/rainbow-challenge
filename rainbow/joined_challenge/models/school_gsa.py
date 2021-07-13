from joined_challenge.models.base import BaseJoinedChallenge


class SchoolGSAJoinedChallenge(BaseJoinedChallenge):

    @property
    def concrete_challenge(self):
        from challenge.models.school_gsa import SchoolGSAChallenge
        return SchoolGSAChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
