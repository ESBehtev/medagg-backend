from django.db.models import Q

from apps.datasets.models import Dataset


class SearchService:
    """
    Search service with business logic.
    """

    def default_datasets(self):
        """Do not return datasets by default"""
        return Dataset.objects.order_by("created_at")[:0]

    def search_datasets(self, query, filter_params):
        """
        Search in datasets by the given query and filter parameters.
        """
        # TODO: Search and filtering
        result_set = (
            Dataset.objects.all()
            .select_related("anatomical_area")
            .prefetch_related("modalities", "ml_tasks", "tags")
        )

        return result_set
