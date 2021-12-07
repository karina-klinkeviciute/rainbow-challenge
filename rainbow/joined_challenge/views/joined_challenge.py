from private_storage.views import PrivateStorageDetailView, PrivateStorageView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, get_object_or_404, CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView

from joined_challenge.models import JoinedChallenge, ArticleJoinedChallenge, EventParticipantJoinedChallenge, \
    SchoolGSAJoinedChallenge, EventOrganizerJoinedChallenge, StoryJoinedChallenge, ProjectJoinedChallenge, \
    ReactingJoinedChallenge, SupportJoinedChallenge, CustomJoinedChallenge, QuizJoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus, JoinedChallengeFile
from joined_challenge.serializers.joined_challenge import (
    JoinedChallengeSerializer,
    ArticleJoinedChallengeSerializer,
    EventParticipantJoinedChallengeSerializer, SchoolGSAJoinedChallengeSerializer,
    EventOrganizerJoinedChallengeSerializer, StoryJoinedChallengeSerializer, ProjectJoinedChallengeSerializer,
    ReactingJoinedChallengeSerializer, SupportJoinedChallengeSerializer, CustomJoinedChallengeSerializer,
    QuizJoinedChallengeSerializer, JoinedChallengeFileSerializer)


class JoinedChallengeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing JoinedChallenge instances.
    """
    serializer_class = JoinedChallengeSerializer
    queryset = JoinedChallenge.objects.all()


class JoinedChallengeFileDetailView(APIView, PrivateStorageDetailView):
    model = JoinedChallengeFile
    model_file_field = 'file'
    content_disposition = 'attachment'

    def can_access_file(self, private_file):
        # When the object can be accessed, the file may be downloaded.
        # This overrides PRIVATE_STORAGE_AUTH_FUNCTION
        return self.request.user.is_admin or self.request.user == private_file.parent_object.joined_challenge.user

    def get_object(self, queryset=None):
        return get_object_or_404(JoinedChallengeFile, file=self.kwargs['path'])


class JoinedChallengeFileUploadView(CreateAPIView):
    queryset = JoinedChallengeFile.objects.all()
    serializer_class = JoinedChallengeFileSerializer

class BaseJoinedChallengeViewset(viewsets.ModelViewSet):
    """Base viewset for joined challenges of dihherent typse"""
    http_method_names = ('get', 'head', 'options', 'post', 'patch', 'delete')

class ArticleJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    A viewset for Article challenges.
    """
    serializer_class = ArticleJoinedChallengeSerializer
    queryset = ArticleJoinedChallenge.objects.all()


class EventParticipantJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    A ViewSet for EventParticipant challenges.
    """
    serializer_class = EventParticipantJoinedChallengeSerializer
    queryset = EventParticipantJoinedChallenge.objects.all()


class SchoolGSAJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    A ViewSet for SchoolGSA challenges.
    """
    serializer_class = SchoolGSAJoinedChallengeSerializer
    queryset = SchoolGSAJoinedChallenge.objects.all()


class EventOrganizerJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = EventOrganizerJoinedChallengeSerializer
    queryset = EventOrganizerJoinedChallenge.objects.all()


class StoryJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = StoryJoinedChallengeSerializer
    queryset = StoryJoinedChallenge.objects.all()


class ProjectJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = ProjectJoinedChallengeSerializer
    queryset = ProjectJoinedChallenge.objects.all()


class ReactingJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = ReactingJoinedChallengeSerializer
    queryset = ReactingJoinedChallenge.objects.all()


class SupportJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = SupportJoinedChallengeSerializer
    queryset = SupportJoinedChallenge.objects.all()


class CustomJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = CustomJoinedChallengeSerializer
    queryset = CustomJoinedChallenge.objects.all()


class QuizJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = QuizJoinedChallengeSerializer
    queryset = QuizJoinedChallenge.objects.all()


class UserJoinedChallengesAPIView(ListAPIView):
    serializer_class = JoinedChallengeSerializer

    def get_queryset(self):
        queryset = JoinedChallenge.objects.all()
        user = self.request.user
        if user is not None:
            queryset = queryset.filter(
                user=user,
                status=JoinedChallengeStatus.JOINED
            )
        return queryset


class UserCompletedChallengesAPIView(ListAPIView):
    serializer_class = JoinedChallengeSerializer

    def get_queryset(self):
        queryset = JoinedChallenge.objects.all()
        user = self.request.user
        if user is not None:
            queryset = queryset.filter(
                user=user,
                status__in=(JoinedChallengeStatus.CONFIRMED, JoinedChallengeStatus.COMPLETED)
            )
        return queryset
