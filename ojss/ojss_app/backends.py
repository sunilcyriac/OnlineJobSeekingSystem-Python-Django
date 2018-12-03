from .models import User


class CustomUserAuth(object):

    def authenticate(self, username=None, password=None):
        try:
            user = User.object.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        try:
            user = User.object.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None