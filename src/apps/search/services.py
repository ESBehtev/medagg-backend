from django.db.models import Q
from kaggle.api.kaggle_api_extended import KaggleApi
from kagglesdk.datasets.types.dataset_api_service import \
    ApiGetDatasetMetadataRequest

from apps.datasets.models import Dataset
from libs.medsearch import api as parser


class SearchService:
    """
    Search service with business logic.
    """

    def __init__(self):
        self.kaggle = KaggleApi()
        self.kaggle.authenticate()

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

    def _build_filters(self, filter_params):
        """Build proper filters"""

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

        return filters, order, distinct

    def _map_kaggle_to_local(self, metadata, dataset):
        """Map Kaggle DatasetInfo and ApiDataset fields to your Dataset model fields"""

        # Extract data from given metadata
        title = metadata.title[:500]
        description = metadata.description
        license_name = ",".join([license.name for license in metadata.licenses])

        # Extract data from given general dataset
        url = dataset.url[:1000]
        size_bytes = dataset.total_bytes

        # FIXME: !!!
        from apps.datasets.models import AnatomicalArea

        area, _ = AnatomicalArea.objects.get_or_create(name="area_1")

        return {
            "title": title,
            "description": description,
            "external_path": url,
            "local_path": None,  # Not applicable for Kaggle datasets
            "record_count": None,  # Kaggle doesn't provide this
            "size": size_bytes,
            "license": license_name,
            "anatomical_area": area,
            # NOTE: Many-to-many fields (modalities, ml_tasks, tags)
            # are handled separately after the Dataset is created
        }

    def search_datasets(self, query, filter_params):
        """
        Get all detailed datasets that match the given query
        and filter them based on the given params.
        ---
        Parameters:
        - query: Search term (title, description)
        - filter_params: Parameters to filter the result set
        """

        search_query = parser.parse_query(query)
        print(f"Search result from medagg-search lib: {search_query}")

        ### Search by title and description in database
        result_set = Dataset.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        ### Search in other source (Kaggle)
        if result_set.count() != 0:
            # TODO: Use updated_at to sync with other sources.
            print("TODO: Not yet implemented")
        else:
            # FIXME: Currently it does 2 request sequentially,
            # do the second one asynchronasly.
            kaggle_datasets = self.kaggle.dataset_list(
                search=query,
                file_type="all",
                sort_by="hottest",
                page=1,
                license_name="all",
            )

            if not kaggle_datasets:
                # We could not find anything in our db as well as in Kaggle.
                return Dataset.objects.none()

            batch_size = 50
            datasets_to_create = []
            for kaggle_dataset in kaggle_datasets:
                (owner_slug, dataset_slug, _) = self.kaggle.dataset_metadata_prep(
                    kaggle_dataset.ref, ""
                )

                with self.kaggle.build_kaggle_client() as kaggle:
                    request = ApiGetDatasetMetadataRequest()
                    request.owner_slug = owner_slug
                    request.dataset_slug = dataset_slug
                    # FIXME: The second request is needed for complete info
                    # about Kaggle's dataset, so for now we do it when searchin'.
                    response = kaggle.datasets.dataset_api_client.get_dataset_metadata(
                        request
                    )

                    if response.error_message:
                        # We could not fetch dataset metadta from Kaggle.
                        break

                    datasets_to_create.append(
                        Dataset(
                            **self._map_kaggle_to_local(response.info, kaggle_dataset)
                        )
                    )

            if len(datasets_to_create) == 0:
                return Dataset.objects.none()

            # Create a bunch of datasets.
            created_datasets = Dataset.objects.bulk_create(
                datasets_to_create, batch_size=batch_size
            )

            # Get QuerySet of created datasets.
            result_set = Dataset.objects.filter(
                id__in=[dataset.id for dataset in created_datasets]
            )

        # Build proper filters
        (filters, order, distinct) = self._build_filters(filter_params)

        # Now, apply aggragation if any is present
        if filters:
            result_set = result_set.filter(**filters)
        if order:
            result_set.order_by(order)
        if distinct:
            result_set.distinct()

        return result_set
