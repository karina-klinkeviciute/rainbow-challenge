from rest_framework import serializers

from results.models.region import Region


class RegionSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Region
        fields = ['name', 'uuid', 'points']
        # fields = '__all__'

    def get_points(self, obj):
        return obj.points
