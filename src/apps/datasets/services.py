from .models import AnatomicalArea, Dataset, MLTask, Modality, Tag


class DatasetService:
    """
    Business logic class for Dataset model.
    """

    def get_one_detailed(self, id):
        """
        Get specific dataset with all known information about it.
        """
        try:
            return (
                Dataset.objects.select_related("anatomical_area")
                .prefetch_related("modalities", "ml_tasks", "tags")
                .get(id=id)
            )
        except Dataset.DoesNotExist:
            # TODO: Handle/log error
            return None

    def get_all_detailed(self):
        """
        Get all datasets with all known information about each one of them.
        """
        return (
            Dataset.objects.all()
            .select_related("anatomical_area")
            .prefetch_related("modalities", "ml_tasks", "tags")
        )
