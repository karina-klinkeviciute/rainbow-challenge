from rest_framework import serializers

from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeFile


class JoinedChallengeFileSerializer(serializers.ModelSerializer):
    """Serializer for files added to joined challenges. """
    class Meta:
        model = JoinedChallengeFile
        fields = ('uuid', 'joined_challenge', 'file', 'file_name')

    file_name = serializers.SerializerMethodField()

    def get_file_name(self, obj):
        """returns only a file name without path"""
        return str(obj.file).split("/")[-1],


class ConcreteJoinedChallengeFileSerializer(serializers.ModelSerializer):
    """Serializer for files added to concrete joined challenges. """
    class Meta:
        model = JoinedChallengeFile
        fields = ('uuid', 'joined_challenge', 'file', 'challenge_type', 'concrete_joined_challenge_uuid', 'file_name')

    challenge_type = serializers.SerializerMethodField()
    concrete_joined_challenge_uuid = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()

    def get_challenge_type(self, obj):
        challenge_type = obj.joined_challenge.challenge.type
        return challenge_type

    def get_concrete_joined_challenge_uuid(self, obj):
        return obj.joined_challenge.concrete_joined_challenge

    def get_file_name(self, obj):
        return str(obj.file).split("/")[-1]


class JoinedChallengeFilesListSerializer(serializers.ModelSerializer):
    """Serializer for the list of files for the main_joined_challenge"""
    class Meta:
        model = JoinedChallenge
        fields = ("files", )

    files = JoinedChallengeFileSerializer(many=True, read_only=True)
