from rest_framework import serializers

from texts.models import Text


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = (
            'title',
            'body',
            'notes',
            'created_at',
            'updated_at'
        )
