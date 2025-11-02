from .models import Dataset


class DatasetService:
    """
    Business logic class for Dataset model.
    """

    def get(self):
        """
        Get specific dataset
        """
        return (
            Dataset.objects.all()
            .select_related("anatomical_area")
            .prefetch_related("modalities", "ml_tasks", "tags")
        )
