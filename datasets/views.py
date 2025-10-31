from rest_framework import generics

from .models import Dataset
from .serializers import DatasetDetailSerializer


class DatasetDetailView(generics.RetrieveAPIView):
    """
    Get detailed information about a specific dataset
    """

    queryset = (
        Dataset.objects.all()
        .select_related("anatomical_area")
        .prefetch_related("modalities", "ml_tasks", "tags")
    )
    serializer_class = DatasetDetailSerializer
