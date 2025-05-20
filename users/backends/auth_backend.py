from ipware import get_client_ip
from users.models import UserModel
from users.utils import normalize_phone, log_login_event

from django.db.models import Q
from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class AuthBackend(BaseBackend):
    """
    Custom authentication backend that allows authentication using email, username, or phone number.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user by checking if the given `username` (email/username/phone)
        matches a user and the password is correct.
        """
        # Normalize username
        username = username.strip().lower() if username else username
        # Normalize phone number
        username = normalize_phone(username.lower().strip())

        try:
            user = UserModel.objects.get(
                Q(email=username) | Q(username=username) | Q(phone_number=username)
            )
        except ObjectDoesNotExist:
            ip, _ = get_client_ip(request)
            ip = ip or "Unknown"

            log_login_event(False, request, username)
            return None
        except MultipleObjectsReturned:
            log_login_event(False, request, username)
            return None

        if user.check_password(password):
            ip, _ = get_client_ip(request)
            ip = ip or "Unknown"

            log_login_event(True, request, username, user.id)
            return user

        ip, _ = get_client_ip(request)
        ip = ip or "Unknown"

        log_login_event(False, request, username)
        return None

    def get_user(self, user_id):
        """
        Retrieve a user instance based on the user ID.
        """
        return UserModel.objects.filter(pk=user_id).first()
