from rest_framework import serializers

from apps.datasets.api.v1.serializers import DatasetDetailedSerializer


class StringListField(serializers.ListField):
    child = serializers.CharField()


class SearchDatasetsGetSerializer(serializers.Serializer):
    """
    All possible filter parameters for the datasets.
    ---
    Make sure to name parameters using the following format:
        <name>_<suffix>
    , where `<name>` is the exact match for the column name in a model
    and `<suffix>` is the special identifier for proper filtering.

    See `app.search.services.search()` for more info.

    Note: Also, `<name>` itself can contain undescores.
    """

    # Filter by anatomical area name
    anatomical_area_name = serializers.CharField(
        required=False, allow_blank=True, min_length=2
    )
    # Minimum record count
    record_count_min = serializers.IntegerField(required=False, allow_null=True)
    # Maximum record count
    record_count_max = serializers.IntegerField(required=False, allow_null=True)
    # Filter by modalities (comma-separated)
    modalities_list = serializers.CharField(required=False, allow_blank=True)
    # Filter by ML tasks (comma-separated)
    ml_tasks_list = serializers.CharField(required=False, allow_blank=True)
    # Filter by tags (comma-separated)
    tags_list = serializers.CharField(required=False, allow_blank=True)
    # Minimum dataset size (MB)
    size_min = serializers.IntegerField(required=False, allow_null=True)
    # Maximum dataset size (MB)
    size_max = serializers.IntegerField(required=False, allow_null=True)
    # Order of resulting datasets
    ordering = serializers.ListField(
        max_length=2,
        default=[
            "created_at",  # Column name to order by
            "desc",  # The exact order (descending)
        ],
    )

    class Meta:
        fields = [
            "anatomical_area_name",
            "record_count_min",
            "record_count_max",
            "modalities_list",
            "ml_tasks_list",
            "tags_list",
            "size_min",
            "size_max",
            "ordering",
        ]


class SearchDatasetsPostSerializer(serializers.Serializer):
    # TODO: Extract length values to constants
    query = serializers.CharField(
        max_length=100,
        min_length=2,
        allow_blank=False,  # TODO: Consider allow_blank=True
    )

    class Meta:
        fields = ["query"]


class SearchDatasetsRequestSerializer(serializers.Serializer):
    # GET query params
    get = SearchDatasetsGetSerializer()
    # POST data
    post = SearchDatasetsPostSerializer()


class SearchResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = DatasetDetailedSerializer(many=True)
