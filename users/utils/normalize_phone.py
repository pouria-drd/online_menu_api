import re


def normalize_phone(phone: str) -> str:
    """
    Convert Persian numbers to English and remove spaces

    Args:
        phone (str): The phone number to be normalized

    Returns:
        str: The normalized phone number
    """
    persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    return re.sub(r"\s+", "", phone.translate(persian_to_english))
