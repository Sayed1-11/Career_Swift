from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in
    using their email address instead of their username.
    """
    def user_can_authenticate(self, user):
        return True

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        # Check by email OR username
        users = UserModel.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username)
        ).order_by('id')
        
        for user in users:
            if user.check_password(password):
                if self.user_can_authenticate(user):
                    return user
                else:
                    # In Django 2.1+, ModelBackend rejects inactive users at authentication layer,
                    # but if we want AuthenticationForm's 'inactive' error to show, we must let it pass
                    pass
        
        return None
