from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic


class UserRegistrationView(generic.View):
    """
    API endpoint that allows to register new user.
    """

    def post(self, request, *args, **kwargs):
        """Register new user"""

        return HttpResponseRedirect("New user created")


class UserLoginView(generic.View):
    """
    API endpoint that allows user to login.
    """

    def post(self, request, *args, **kwargs):
        """Authenticate a user"""

        return HttpResponseRedirect("You are logged in")


class UserProfileView(generic.View):
    """
    API endpoint that allows to get user info.
    """

    def get(self, request, *args, **kwargs):
        """Get user personal data and return it"""

        return HttpResponse("Aleksey Bogomolov")
