from .models import Group, User


class UserService:
    """
    Business logic class for User model.
    """

    def get_all(self, order_by):
        """
        Get all users ordered by the given parameter.
        """
        return User.objects.all().order_by(order_by)


class GroupService:
    """
    Business logic class for Group model.
    """

    def get_all(self, order_by):
        """
        Get all groups ordered by the given parameter.
        """
        return Group.objects.all().order_by(order_by)
