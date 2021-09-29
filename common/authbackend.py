from django.contrib.auth.backends import ModelBackend

from common.const import ROOT
from module.user.models import User


class AuthRootBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        user_type = getattr(user, 'type', None)
        return bool(user_type == ROOT)
