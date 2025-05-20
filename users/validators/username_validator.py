from django.core.validators import RegexValidator

# Username Validator
username_validator = RegexValidator(
    regex=r"^[a-z0-9_]{1,25}$",
    message="Username can only contain lowercase letters, numbers, and underscores and must be at most 25 characters long.",
    code="invalid_username",
)
