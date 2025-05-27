import re


def normalize_phone(phone: str) -> str:
    """
    Convert Persian numbers to English, remove spaces,
    and convert local Iranian phone numbers starting with 0
    to international format starting with +98.

    Args:
        phone (str): The phone number to be normalized

    Returns:
        str: The normalized phone number in international format
    """
    persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    phone = phone.translate(persian_to_english)
    phone = re.sub(r"\s+", "", phone)

    # If local Iranian phone (0XXXXXXXXX), convert to +98XXXXXXXXX
    if re.match(r"^0\d{10}$", phone):
        phone = "+98" + phone[1:]
    # else:
    #     # If it doesn't start with '+' after normalization, warn
    #     if not phone.startswith("+"):
    #         print(" [WARNING] Invalid phone format:", phone)

    return phone
