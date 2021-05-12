from challenge.models import EventParticipantChallenge
from challenge.models.joined_challenge.base import BaseJoinedChallenge


class EventParticipantJoinedChallenge(BaseJoinedChallenge):

    @property
    def concrete_challenge(self):
        return EventParticipantChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
