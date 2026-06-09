from django.apps import apps
from private_storage.views import PrivateStorageDetailView
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from challenge.models.base import ChallengeType
from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeFile
from joined_challenge.serializers.files import JoinedChallengeFileSerializer, JoinedChallengeFilesListSerializer, \
    ConcreteJoinedChallengeFileSerializer


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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # A user may only attach files to their own joined challenges.
        joined_challenge = serializer.validated_data["joined_challenge"]
        if joined_challenge.user != self.request.user:
            raise PermissionDenied
        serializer.save()


class JoinedChallengeFilesListView(RetrieveAPIView):
    serializer_class = JoinedChallengeFilesListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return JoinedChallenge.objects.filter(user=self.request.user)


class ConcreteJoinedChallengeFilesListView(APIView):
    """Class to get file list for """
    permission_classes = [IsAuthenticated]

    def get(self, request, challenge_type, uuid, format=None):

        joined_challenge_class = ChallengeType.JOINED_CHALLENGE_CLASSES[challenge_type]
        model = apps.get_model('joined_challenge', joined_challenge_class)
        joined_challenge = get_object_or_404(model, uuid=uuid)
        main_joined_challenge = joined_challenge.main_joined_challenge
        # Through the API, only the owning user may access their joined challenge
        # files; cross-user access is reserved for the Django admin interface.
        if main_joined_challenge.user != request.user:
            raise PermissionDenied
        files = JoinedChallengeFileSerializer(main_joined_challenge.files, many=True)
        return Response(files.data)


class ConcreteJoinedChallengeFileUploadView(CreateAPIView):
    """View for uploading files when only having the concrete joined challenge uuid and not main joined challenge."""
    queryset = JoinedChallengeFile.objects.all()
    serializer_class = ConcreteJoinedChallengeFileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        challenge_type = request.data.get("challenge_type")
        concrete_challenge_uuid = request.data.get("concrete_joined_challenge_uuid")

        joined_challenge_class = ChallengeType.JOINED_CHALLENGE_CLASSES[challenge_type]
        model = apps.get_model('joined_challenge', joined_challenge_class)
        concrete_joined_challenge = model.objects.get(uuid=concrete_challenge_uuid)
        joined_challenge = concrete_joined_challenge.main_joined_challenge
        # A user may only attach files to their own joined challenges.
        if joined_challenge.user != request.user:
            raise PermissionDenied
        request.data["joined_challenge"] = joined_challenge.uuid
        return super().post(request, *args, **kwargs)
