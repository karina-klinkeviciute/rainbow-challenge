from joined_challenge.models.base import BaseJoinedChallenge


class EventParticipantJoinedChallenge(BaseJoinedChallenge):

    @property
    def concrete_challenge(self):
        from challenge.models import EventParticipantChallenge
        return EventParticipantChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
