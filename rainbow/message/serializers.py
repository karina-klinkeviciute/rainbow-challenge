from rest_framework import serializers

from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "uuid",
            "message_text",
            "user",
            "admin_sender",
            "time_sent",
            "seen",
        )
        read_only_fields = (
            "uuid",
            "message_text",
            "user",
            "admin_sender",
            "time_sent",
        )
