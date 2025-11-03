from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.datasets.services import DatasetService
from apps.search.services import SearchService

from .serializers import SearchRequestSerializer, SearchResponseSerializer


class BaseSearchViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset that provides `create` only action.

    To use it:
    1. Override the class and set the `.queryset` and `.serializer_class` attributes.
    2. Override `.search()` method and handle search request as query_params or POST.
    """

    def search(self, request):
        return self.get_queryset()

    def create(self, request):
        return self.search(request=request)


class SearchDatasetsViewSet(BaseSearchViewSet):
    """
    Search datasets API endpoint that allows datasets to be searched with query.
    """

    @property
    def _search_service(self):
        return SearchService()

    def get_serializer_class(self):
        return SearchRequestSerializer

    def get_queryset(self):
        return self._search_service.default_datasets()

    def search(self, request):
        """Search for datasets"""
        # TODO: Parse data
        result_set = self._search_service.search_datasets(
            query="",
            filter_params={},
        )

        serializer = SearchResponseSerializer(
            {"count": result_set.count(), "results": result_set}
        )
        return Response(serializer.data)
