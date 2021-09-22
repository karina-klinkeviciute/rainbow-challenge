from django.contrib.auth import get_user_model
from djoser.conf import settings
from rest_framework import serializers
from djoser.compat import get_user_email, get_user_email_field_name

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    all_points = serializers.IntegerField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
        ) + (
            'gender',
            'gender_other',
            'username',
            'region',
            'is_lgbtqia',
            # 'completed_joined_challenges',
            'all_points',
            'remaining_points',
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=["is_active"])
        return super().update(instance, validated_data)


class GenderSerializer(serializers.Serializer):
    genders = serializers.DictField()
