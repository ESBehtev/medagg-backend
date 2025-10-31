from rest_framework import serializers

from datasets.models import UserSearchQuery
from datasets.serializers import DatasetListSerializer


class SearchQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSearchQuery
        fields = ["id", "query_text", "filters", "performed_at"]


class SearchResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = DatasetListSerializer(many=True)

    class Meta:
        fields = ["count", "results"]
