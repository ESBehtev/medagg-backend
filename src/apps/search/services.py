from django.db.models import Q

from apps.datasets.models import Dataset
from libs.medsearch import api as parser


class SearchService:
    """
    Search service with business logic.
    """

    def default_datasets(self):
        """Retrieve the last 5 created datasets, just in case"""
        return Dataset.objects.order_by("created_at")[:5]

    @property
    def _filter_exclude_suffixes(self):
        """Suffixes to exclude from filtering."""
        return "_ex"

    @property
    def _filter_single_suffixes(self):
        """Suffixes to remove and/or replace"""
        return {"_id": "__id", "_name": "__name", "_min": "__gte", "_max": "__lte"}

    @property
    def _filter_list_suffixes(self):
        """
        List suffixes to remove and/or replace.

        Lists are handled separately due to the specifics of
        working with them.
        """
        return {"_list": "__name__in", "_id_list": "__id__in"}

    def search_datasets(self, query, filter_params):
        """
        Get all detailed datasets that match the given query
        and filter them based on the given params.
        ---
        Parameters:
        - query: Search term (title, description)
        - filter_params: Parameters to filter the result set
        """

        search_result = parser.parse_query(query)
        print(f"Search result from medagg-search lib: {search_result}")

        # Search by title and description
        result_set = Dataset.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        # Build proper filters
        filters = {}
        order = ""  # Store the correct argument for quering
        distinct = False
        for name, value in filter_params.items():
            # Ignore empty params
            if not value:
                continue

            # Exclude specified params
            if name.endswith(self._filter_exclude_suffixes):
                continue

            # There should be always some ordering
            if name.startswith("order"):
                order = "-" + value[0] if value[1] == "desc" else value[0]
                continue

            # Extract filters with multiple values
            for k, v in self._filter_list_suffixes.items():
                if name.endswith(k):
                    filters[name.replace(k, v)] = value.split(",")
                    distinct = True
                    break
            if distinct:
                continue

            # Extract filters with special aggregation
            for k, v in self._filter_single_suffixes.items():
                if name.endswith(k):
                    filters[name.replace(k, v)] = value
                    break
            else:
                # Extract every other filter
                filters[name] = value

        # Now, apply aggragation if any is present
        if filters:
            result_set = result_set.filter(**filters)
        if order:
            result_set.order_by(order)
        if distinct:
            result_set.distinct()

        return result_set
