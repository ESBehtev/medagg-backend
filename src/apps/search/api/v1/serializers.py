from rest_framework import serializers

from apps.datasets.api.v1.serializers import DatasetListSerializer


class SearchResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = DatasetListSerializer(many=True)

    class Meta:
        fields = ["count", "results"]
