from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from apps.datasets.services import DatasetService

from .serializers import DatasetDetailedSerializer
class DatasetsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Datasets API endpoint that allows datasets to be viewed only.
    """

    serializer_class = DatasetDetailedSerializer

    @property
    def _dataset_service(self):
        return DatasetService()

    def get_queryset(self):
        return self._dataset_service.get_all_detailed()

    def list(self, request):
        """
        Get all datasets with detailed information about each dataset
        """
        datasets = self.get_queryset()
        serializer = self.get_serializer(datasets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Get detailed information about a specific dataset
        """
        if not pk:
            return Response("Provide primary key", status=status.HTTP_400_BAD_REQUEST)

        dataset = self._dataset_service.get_one_detailed(id=pk)
        if not dataset:
            return Response("Dataset does not exist", status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(dataset)
        return Response(serializer.data)
