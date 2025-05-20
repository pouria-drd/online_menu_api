from django.core.validators import EmailValidator

# Email Validator
email_validator = EmailValidator(
    message="Enter a valid email address.",
    code="invalid_email",
)
