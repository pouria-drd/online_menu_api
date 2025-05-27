import re
from ipware import get_client_ip
from users.models import UserModel
from users.utils import normalize_phone, log_login_event

from django.db.models import Q
from django.contrib.auth.backends import BaseBackend


class AuthBackend(BaseBackend):
    """
    Custom authentication backend allowing login by email, username, or phone number.
    Phone numbers are normalized to handle Iranian formats.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        username = username.strip()

        # Determine if username looks like a phone number (digits or Persian digits)
        if re.search(r"[0-9۰-۹]", username):
            normalized_phone = normalize_phone(username)
        else:
            normalized_phone = None

        # Normalize email and username to lowercase
        username_lower = username.lower()

        user = None
        try:
            if normalized_phone:
                # Try phone lookup first if phone-like input
                user = UserModel.objects.get(phone_number=normalized_phone)
            else:
                # Otherwise, try email or username lookup
                user = UserModel.objects.get(
                    Q(email=username_lower) | Q(username=username_lower)
                )
        except UserModel.DoesNotExist:
            self._log_failed_login(request, username, reason="User not found")
            return None
        except UserModel.MultipleObjectsReturned:
            self._log_failed_login(request, username, reason="Multiple users found")
            return None

        if user.check_password(password):
            self._log_successful_login(request, username)
            return user
        else:
            self._log_failed_login(request, username, reason="Incorrect password")
            return None

    def get_user(self, user_id):
        return UserModel.objects.filter(pk=user_id).first()

    def _log_failed_login(self, request, username, reason=""):
        ip, _ = get_client_ip(request)
        ip = ip or "Unknown"
        log_login_event(False, request, username, reason=reason)

    def _log_successful_login(self, request, username):
        ip, _ = get_client_ip(request)
        ip = ip or "Unknown"
        log_login_event(True, request, username)
