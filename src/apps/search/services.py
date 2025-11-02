from django.db.models import Q

from apps.datasets.models import AnatomicalArea, Dataset, MLTask, Modality, Tag


class SearchService:
    """
    Search service with business logic.
    """

    def get_all(
        self,
        q,
        anatomical_area_id,
        modalities_ids,
        ml_tasks_ids,
        tags_ids,
        min_records,
        max_records,
        min_size,
        max_size,
        ordering,
    ):
        """
        Get all datasets with filters
        ---
        Parameters:
        - q: Search term (title, description)
        - anatomical_area: Filter by anatomical area ID
        - modalities: Filter by modality IDs (comma-separated)
        - ml_tasks: Filter by ML task IDs (comma-separated)
        - tags: Filter by tag IDs (comma-separated)
        - min_records: Minimum record count
        - max_records: Maximum record count
        - min_size: Minimum dataset size (byte)
        - max_size: Maximum dataset size (byte)
        - ordering: Order of datasets in resulting set
        """
        result_set = (
            Dataset.objects.all()
            .select_related("anatomical_area")
            .prefetch_related("modalities", "ml_tasks", "tags")
        )

        # Search by the given term
        if q:
            result_set = result_set.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )

        # Apply filters
        if anatomical_area_id:
            result_set = result_set.filter(anatomical_area_id=anatomical_area_id)

        if modalities_ids:
            modalities_list = [int(x) for x in modalities_ids.split(",")]
            result_set = result_set.filter(
                modalities__id__in=modalities_list
            ).distinct()

        if ml_tasks_ids:
            ml_tasks_list = [int(x) for x in ml_tasks_ids.split(",")]
            result_set = result_set.filter(ml_tasks__id__in=ml_tasks_list).distinct()

        if tags_ids:
            tags_list = [int(x) for x in tags_ids.split(",")]
            result_set = result_set.filter(tags__id__in=tags_list).distinct()

        if min_records:
            result_set = result_set.filter(record_count__gte=int(min_records))

        if max_records:
            result_set = result_set.filter(record_count__lte=int(max_records))

        if min_size:
            result_set = result_set.filter(size__gte=int(min_size))

        if max_size:
            result_set = result_set.filter(size__lte=int(max_size))

        if ordering:
            result_set = result_set.order_by(ordering)

        return result_set

    def get_all_filters(self):
        """
        Get available filter options
        """
        return {
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
