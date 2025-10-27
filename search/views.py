from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic


class QueryView(generic.View):
    """
    API endpoint that allows to query datasets to be viewed.
    """

    def post(self, request, *args, **kwargs):
        """Redirect somewhere, e.g. to user profile."""

        return HttpResponseRedirect("Found something")
