from rest_framework import permissions, viewsets
from rest_framework.response import Response

from apps.users.services import GroupService, UserService

from .serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User API endpoint that allows users to be viewed only.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @property
    def _user_service(self):
        return UserService()

    def get_queryset(self):
        return self._user_service.get_all(order_by="-date_joined")

    def list(self, request):
        """
        Get all users.
        """
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Get a specific user.
        """
        if not pk:
            return Response("Provide primary key")
        user = self._user_service.get_one(id=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Group API endpoint that allows groups to be viewed only.
    """

    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @property
    def _group_service(self):
        return GroupService()

    def get_queryset(self):
        return self._group_service.get_all(order_by="-date_joined")

    def list(self, request):
        """
        Get all groups
        """
        groups = self.get_queryset()
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Get a specific group
        """
        if not pk:
            return Response("Provide primary key")
        group = self._group_service.get_one(id=pk)
        serializer = self.get_serializer(group)
        return Response(serializer.data)
