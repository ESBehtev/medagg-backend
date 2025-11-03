from rest_framework import serializers

from apps.datasets.api.v1.serializers import DatasetDetailedSerializer


class SearchRequestSerializer(serializers.Serializer):
    # TODO: Extract length values to constants
    query = serializers.CharField(
        max_length=100, min_length=2, allow_blank=False, trim_whitespace=False
    )

    class Meta:
        fields = ["query"]


class SearchResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = DatasetDetailedSerializer(many=True)

    class Meta:
        fields = ["count", "results"]
