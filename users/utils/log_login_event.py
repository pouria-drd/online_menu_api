from logging import getLogger
from ipware import get_client_ip
from django.utils.timezone import now
from rest_framework.request import Request

logger = getLogger("login_v1")


def log_login_event(success: bool, request: Request, username: str, reason: str = None):
    """
    Log a login event with the given success status, request, username, and optional reason.

    Args:
        success (bool): Whether the login was successful
        request (Request): The request object
        username (str): The username or email used for login
        reason (str, optional): Additional reason or context for the login event
    """
    ip, _ = get_client_ip(request)
    ip = ip or "Unknown"
    status = "success" if success else "failure"
    user_info = f"Username: {username}"
    reason_info = f", Reason: {reason}" if reason else ""

    log_message = f"Login {status}. URL: {request.build_absolute_uri()}, {user_info}, IP: {ip}, Time: {now()}{reason_info}"

    if success:
        logger.info(log_message)
    else:
        logger.warning(log_message)
