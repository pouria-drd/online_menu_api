from django.core.validators import RegexValidator

# Iranian Phone Number Validator
iran_phone_validator = RegexValidator(
    regex=r"^\+98(9\d{9})$",
    message="Enter a valid Iranian phone number (e.g., +989123456789).",
    code="invalid_phone",
)
