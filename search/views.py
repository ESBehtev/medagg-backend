from django.db.models import Q
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from datasets.models import AnatomicalArea, Dataset, MLTask, Modality, Tag
from datasets.serializers import DatasetListSerializer


class SearchViewSet(viewsets.ViewSet):
    """
    Search API for datasets
    """

    def list(self, request):
        """
        Search datasets with filters
        ---
        Parameters:
        - q: Search term (title, description)
        - anatomical_area: Filter by anatomical area ID
        - modalities: Filter by modality IDs (comma-separated)
        - ml_tasks: Filter by ML task IDs (comma-separated)
        - tags: Filter by tag IDs (comma-separated)
        - min_records: Minimum record count
        - max_records: Maximum record count
        - min_size: Minimum dataset size (MB)
        - max_size: Maximum dataset size (MB)
        """
        queryset = (
            Dataset.objects.all()
            .select_related("anatomical_area")
            .prefetch_related("modalities", "ml_tasks", "tags")
        )

        # Search by the given term
        search_term = request.GET.get("q")
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) | Q(description__icontains=search_term)
            )

        # Apply filters
        anatomical_area_id = request.GET.get("anatomical_area")
        if anatomical_area_id:
            queryset = queryset.filter(anatomical_area_id=anatomical_area_id)

        modalities_ids = request.GET.get("modalities")
        if modalities_ids:
            modalities_list = [int(x) for x in modalities_ids.split(",")]
            queryset = queryset.filter(modalities__id__in=modalities_list).distinct()

        ml_tasks_ids = request.GET.get("ml_tasks")
        if ml_tasks_ids:
            ml_tasks_list = [int(x) for x in ml_tasks_ids.split(",")]
            queryset = queryset.filter(ml_tasks__id__in=ml_tasks_list).distinct()

        tags_ids = request.GET.get("tags")
        if tags_ids:
            tags_list = [int(x) for x in tags_ids.split(",")]
            queryset = queryset.filter(tags__id__in=tags_list).distinct()

        min_records = request.GET.get("min_records")
        if min_records:
            queryset = queryset.filter(record_count__gte=int(min_records))

        max_records = request.GET.get("max_records")
        if max_records:
            queryset = queryset.filter(record_count__lte=int(max_records))

        min_size = request.GET.get("min_size")
        if min_size:
            queryset = queryset.filter(size__gte=int(min_size))

        max_size = request.GET.get("max_size")
        if max_size:
            queryset = queryset.filter(size__lte=int(max_size))

        ordering = request.GET.get("ordering", "-created_at")
        if ordering:
            queryset = queryset.order_by(ordering)

        serializer = DatasetListSerializer(queryset, many=True)
        return Response({"count": queryset.count(), "results": serializer.data})

    @action(detail=False, methods=["get"])
    def filters(self, request):
        """
        Get available filter options
        """
        return Response(
            {
                "anatomical_areas": [
                    {"id": area.id, "name": area.name}
                    for area in AnatomicalArea.objects.all()
                ],
                "modalities": [
                    {"id": modality.id, "name": modality.name}
                    for modality in Modality.objects.all()
                ],
                "ml_tasks": [
                    {"id": task.id, "name": task.name} for task in MLTask.objects.all()
                ],
                "tags": [{"id": tag.id, "name": tag.name} for tag in Tag.objects.all()],
            }
        )
