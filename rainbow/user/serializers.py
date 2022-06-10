from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework import serializers
from djoser.compat import get_user_email, get_user_email_field_name

from results.serializers.medal import MedalSerializer
from results.serializers.region import RegionSerializer

User = get_user_model()


class CustomUserCreateSerializer(UserCreatePasswordRetypeSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
        ) + (
             'password',
             'gender',
             'gender_other',
             'username',
             'region',
             'year_of_birth',
         )


class UserSerializer(serializers.ModelSerializer):
    all_points = serializers.IntegerField()
    region = RegionSerializer()

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
            'year_of_birth',
            # 'is_lgbtqia',
            'all_points',
            'remaining_points',
            'streak',
            'medals'
        )
        read_only_fields = (settings.LOGIN_FIELD, 'all_points', 'remaining_points', 'streak', 'medals')

    medals = MedalSerializer(many=True)

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
