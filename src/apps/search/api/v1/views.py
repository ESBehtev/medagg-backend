from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.search.services import SearchService

from .serializers import SearchResponseSerializer


class SearchViewSet(viewsets.ViewSet):
    """
    Search API for datasets
    """

    @property
    def _search_service(self):
        return SearchService()

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
        - ordering: Order of datasets in resulting set
        """
        queryset = self._search_service.get_all(
            q=request.GET.get("q"),
            anatomical_area_id=request.GET.get("anatomical_area"),
            modalities_ids=request.GET.get("modalities"),
            ml_tasks_ids=request.GET.get("ml_tasks"),
            tags_ids=request.GET.get("tags"),
            min_records=request.GET.get("min_records"),
            max_records=request.GET.get("max_records"),
            min_size=request.GET.get("min_size"),
            max_size=request.GET.get("max_size"),
            ordering=request.GET.get("ordering", "-created_at"),
        )

        serializer = SearchResponseSerializer(
            {"count": queryset.count(), "results": queryset}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def filters(self, request):
        """
        Get available filter options
        """
        return Response(self._search_service.get_all_filters())
