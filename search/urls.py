from django.urls import path

from . import views

app_name = "search"
urlpatterns = [
    # ex: /search - POST
    path("", views.QueryView.as_view(), name="query"),
]
