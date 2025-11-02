from rest_framework import generics

from apps.datasets.services import DatasetService

from .serializers import DatasetDetailSerializer


class DatasetDetailView(generics.RetrieveAPIView):
    """
    Get detailed information about a specific dataset
    """

    serializer_class = DatasetDetailSerializer

    @property
    def _dataset_service(self):
        return DatasetService()

    def get_qeryset(self):
        return self._dataset_service.get()
