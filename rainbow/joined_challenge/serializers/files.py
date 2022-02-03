from rest_framework import serializers

from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeFile


class JoinedChallengeFileSerializer(serializers.ModelSerializer):
    """Serializer for files added to joined challenges. """
    class Meta:
        model = JoinedChallengeFile
        fields = ('uuid', 'joined_challenge', 'file')


class JoinedChallengeFilesListSerializer(serializers.ModelSerializer):
    """Serializer for the list of files for the main_joined_challenge"""
    class Meta:
        model = JoinedChallenge
        fields = ("files", )

    files = JoinedChallengeFileSerializer(many=True, read_only=True)
