from rest_framework import serializers

from news.models import NewsItem


class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = (
            'title',
            'body',
            'image',
            'created_at'
        )
