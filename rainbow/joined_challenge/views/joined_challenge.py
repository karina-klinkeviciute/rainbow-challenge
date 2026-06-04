from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from challenge.models import EventParticipantChallenge
from joined_challenge.models import JoinedChallenge, ArticleJoinedChallenge, EventParticipantJoinedChallenge, \
    SchoolGSAJoinedChallenge, EventOrganizerJoinedChallenge, StoryJoinedChallenge, ProjectJoinedChallenge, \
    ReactingJoinedChallenge, SupportJoinedChallenge, CustomJoinedChallenge, QuizJoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus
from joined_challenge.models.quiz import UserAnswer
from joined_challenge.permissions import UserOwnedQuerysetMixin
from joined_challenge.serializers.joined_challenge import (
    JoinedChallengeSerializer,
    ArticleJoinedChallengeSerializer,
    EventParticipantJoinedChallengeSerializer, SchoolGSAJoinedChallengeSerializer,
    EventOrganizerJoinedChallengeSerializer, StoryJoinedChallengeSerializer, ProjectJoinedChallengeSerializer,
    ReactingJoinedChallengeSerializer, SupportJoinedChallengeSerializer, CustomJoinedChallengeSerializer,
    QuizJoinedChallengeSerializer, UserAnswerSerializer, QRCodeScanSerializer)


class JoinedChallengeViewSet(UserOwnedQuerysetMixin, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing JoinedChallenge instances.
    """
    serializer_class = JoinedChallengeSerializer
    queryset = JoinedChallenge.objects.all()


class BaseJoinedChallengeViewset(UserOwnedQuerysetMixin, viewsets.ModelViewSet):
    """Base viewset for joined challenges of different types.

    Access is restricted to the owning user via ``UserOwnedQuerysetMixin``;
    the concrete challenges link to their user through ``main_joined_challenge``.
    """
    http_method_names = ('get', 'head', 'options', 'post', 'patch', 'delete')
    owner_lookup_field = 'main_joined_challenge__user'


class ArticleJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Article.
    """
    serializer_class = ArticleJoinedChallengeSerializer
    queryset = ArticleJoinedChallenge.objects.all()


class EventParticipantJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Event Participant.
    """
    serializer_class = EventParticipantJoinedChallengeSerializer
    queryset = EventParticipantJoinedChallenge.objects.all()


class QRCodeScanView(APIView):
    """
    A view for joining and completing any event challenge
    """
    serializer_class = QRCodeScanSerializer

    def post(self, request, format=None):
        qr_code = request.data.get("qr_code")
        serializer = QRCodeScanSerializer(data={"qr_code": qr_code}, context={"user": self.request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SchoolGSAJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type School GSA.
    """
    serializer_class = SchoolGSAJoinedChallengeSerializer
    queryset = SchoolGSAJoinedChallenge.objects.all()


class EventOrganizerJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Event Organizer.
    """
    serializer_class = EventOrganizerJoinedChallengeSerializer
    queryset = EventOrganizerJoinedChallenge.objects.all()


class StoryJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Story.
    """
    serializer_class = StoryJoinedChallengeSerializer
    queryset = StoryJoinedChallenge.objects.all()


class ProjectJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Project.
    """
    serializer_class = ProjectJoinedChallengeSerializer
    queryset = ProjectJoinedChallenge.objects.all()


class ReactingJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Reacting.
    """
    serializer_class = ReactingJoinedChallengeSerializer
    queryset = ReactingJoinedChallenge.objects.all()


class SupportJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Support.
    """
    serializer_class = SupportJoinedChallengeSerializer
    queryset = SupportJoinedChallenge.objects.all()


class CustomJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Custom.
    """
    serializer_class = CustomJoinedChallengeSerializer
    queryset = CustomJoinedChallenge.objects.all()


class QuizJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Quiz.
    """
    serializer_class = QuizJoinedChallengeSerializer
    queryset = QuizJoinedChallenge.objects.all()


class UserAnswerViewSet(UserOwnedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = UserAnswerSerializer
    queryset = UserAnswer.objects.all()
    owner_lookup_field = 'quiz_joined_challenge__main_joined_challenge__user'


class UserJoinedChallengesAPIView(ListAPIView):
    serializer_class = JoinedChallengeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JoinedChallenge.objects.filter(
            user=self.request.user,
            status=JoinedChallengeStatus.JOINED
        )


class UserCompletedChallengesAPIView(ListAPIView):
    serializer_class = JoinedChallengeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JoinedChallenge.objects.filter(
            user=self.request.user,
            status__in=(JoinedChallengeStatus.CONFIRMED, JoinedChallengeStatus.COMPLETED)
        )
