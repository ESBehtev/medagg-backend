from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.search.services import SearchService

from .serializers import (SearchDatasetsGetSerializer,
                          SearchDatasetsPostSerializer,
                          SearchDatasetsRequestSerializer,
                          SearchResponseSerializer)


class BaseSearchViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset that provides `create` only action.

    To use it:
    1. Override the class and set the `.queryset` and `.serializer_class` attributes.
    2. Override `.search()` method and handle search request with POST `.data`.
    """

    def search(self, request):
        return self.get_queryset()

    def create(self, request):
        return self.search(request=request)


class SearchDatasetsViewSet(BaseSearchViewSet):
    """
    Search API endpoint that allows datasets to be searched with query.
    """

    @property
    def _search_service(self):
        return SearchService()

    def get_serializer_class(self):
        return SearchDatasetsPostSerializer

    def get_queryset(self):
        return self._search_service.default_datasets()

    def search(self, request):
        """Get filtered datasets"""

        # POST data is already initialized, so we need to
        # combine it with GET query params and check if it's valid.
        req_serializer = SearchDatasetsRequestSerializer(
            # TODO: Extract this to some middleware where the request is serialized by ViewSet
            data={"get": request.query_params, "post": request.data}
        )
        if not req_serializer.is_valid():
            return Response(req_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Search for datasets using the given query
        result_set = self._search_service.search_datasets(
            query=req_serializer.data["post"]["query"],
            filter_params=req_serializer.data["get"],
        )

        # Serialize the response
        res_serializer = SearchResponseSerializer(
            {"count": result_set.count(), "results": result_set}
        )
        return Response(res_serializer.data)

    @action(detail=False, methods=["get"])
    def filters(self, request):
        """Get available filter options"""
        # TODO: Extract filters from SearchDatasetsFilterParamsSerializer
        pass
