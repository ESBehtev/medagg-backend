from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "datasets"

router = DefaultRouter()

router.register(r"", views.DatasetsViewSet, basename="dataset-list")

"""
Add aditional urls that are not part of ViewSets.
Note: Remember that every added bewlow will be part
of 'datasets/' url-prefix.

For example:
urlpatterns = [
    path("foo", views.BarBazView.as_view(), name="foo-bar"),
]
"""
urlpatterns = []

# Combine ViewSet's urls with others
urlpatterns += router.urls
