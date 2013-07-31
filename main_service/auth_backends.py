from django.contrib.auth.backends import ModelBackend
from models import eGazeciarzUser
import hashlib

class eGazeciarzAuthenticationBackend(ModelBackend):
    joomla_pwsecret = ''

    def authenticate(self, username=None, password=None, **kwargs):

        if username == '':
            return None
        try:
            user = eGazeciarzUser.objects.get(username__exact = username)
            pass_db = user.password.split(":")
            encoded_password = pass_db[0]

            salt = self.joomla_pwsecret + pass_db[1]

            m = hashlib.md5()
            m.update(password + salt)
            hex = m.hexdigest()
            if encoded_password == hex:
                return user
            else:
                return None

        except eGazeciarzUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return eGazeciarzUser.objects.get(id = user_id)
        except eGazeciarzUser.DoesNotExist:
            return None
