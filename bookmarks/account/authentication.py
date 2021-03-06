from django.contrib.auth.models import User

class EmailAuthentication(object):
    """
    Authenticate using an e-mail addres.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.object.get(pk=user_id)
        except User.DoesNotExist:
            return None