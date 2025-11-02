from rest_framework import permissions, viewsets

from apps.users.services import GroupService, UserService

from .serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @property
    def _user_service(self):
        return UserService()

    def get_queryset(self):
        return self._user_service.get_all(order_by="-date_joined")


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @property
    def _group_service(self):
        return GroupService()

    def get_queryset(self):
        return self._group_service.get_all(order_by="name")
