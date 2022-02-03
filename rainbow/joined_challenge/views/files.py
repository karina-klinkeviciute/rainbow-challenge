from django.apps import apps
from private_storage.views import PrivateStorageDetailView
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from challenge.models.base import ChallengeType
from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeFile
from joined_challenge.serializers.files import JoinedChallengeFileSerializer, JoinedChallengeFilesListSerializer


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


@permission_classes([IsAuthenticated])
class JoinedChallengeFilesListView(RetrieveAPIView):
    serializer_class = JoinedChallengeFilesListSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return JoinedChallenge.objects.filter(user=self.request.user)


class ConcreteJoinedChallengeFilesList(APIView):
    """Class to get file list for """
    def get(self, request, challenge_type, uuid, format=None):

        joined_challenge_class = ChallengeType.JOINED_CHALLENGE_CLASSES[challenge_type]
        model = apps.get_model('joined_challenge', joined_challenge_class)
        joined_challenge = model.objects.get(uuid=uuid)
        files = JoinedChallengeFileSerializer(joined_challenge.main_joined_challenge.files, many=True)
        return Response(files.data)
