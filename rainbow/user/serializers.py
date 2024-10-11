from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from djoser.conf import settings
from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework import serializers
from djoser.compat import get_user_email, get_user_email_field_name

from results.models import Region
from results.serializers.medal import MedalSerializer
from results.serializers.region import RegionSerializer
from results.utils import message_site_admins


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
        if 'region' in validated_data:
            validated_data.pop("region")
        if 'region' in self.initial_data:
            region_uuid = self.initial_data.get("region").get("uuid")
            region = Region.objects.get(uuid=region_uuid)
            instance.region = region
            instance.save()
        email_field = get_user_email_field_name(User)
        if settings.SEND_ACTIVATION_EMAIL and (email_field in validated_data):
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=["is_active"])
        return super().update(instance, validated_data)

    def delete(self, instance):
        instance.marked_for_deletion = True
        instance.marked_for_deletion_date = datetime.now()
        instance.save()
        message_site_admins(
            _("A user wants to delete account"),
            _("User has marked account for deletion. Please take care of it.")
        )

class GenderSerializer(serializers.Serializer):
    genders = serializers.DictField()
