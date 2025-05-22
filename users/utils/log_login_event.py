from logging import getLogger
from ipware import get_client_ip
from django.utils.timezone import now
from rest_framework.request import Request

logger = getLogger("login_v1")


def log_login_event(success: bool, request: Request, username: str):
    """
    Log a login event with the given success status, request, username, and user ID.

    Args:
        success (bool): Whether the login was successful
        request (Request): The request object
        username (str): The username or email used for login
    """
    ip, _ = get_client_ip(request)
    ip = ip or "Unknown"
    status = "success" if success else "failure"
    user_info = f"Username: {username}"

    if success:
        logger.info(
            f"Login {status}. URL: {request.build_absolute_uri()}, {user_info}, IP: {ip}, Time: {now()}"
        )

    else:
        logger.warning(
            f"Login {status}. URL: {request.build_absolute_uri()}, {user_info}, IP: {ip}, Time: {now()}"
        )
