import uuid
from django.db import models
from users.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.validators import username_validator, iran_phone_validator, email_validator


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that replaces Django's default user model.
    Uses UUID as the primary key, enforces unique usernames, and supports both email and phone authentication.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Email is required for user creation
    email = models.EmailField(
        unique=True,
        blank=False,  # Email is required
        null=False,
        validators=[email_validator],  # Apply email validator
        help_text="Enter a valid email address.",
    )

    # Username is required and must be unique
    username = models.CharField(
        unique=True,
        max_length=25,
        validators=[username_validator],  # Apply username validator
        help_text="Required. 25 characters or fewer. Letters, digits, and _ only.",
    )

    # Phone number is required for user creation
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        blank=False,  # Phone number is required
        null=False,
        validators=[iran_phone_validator],  # Apply phone number validator
        help_text="Enter a valid Iranian phone number (e.g., +989123456789).",
    )

    # Optional last name field, can be left blank or set to null.
    last_name = models.CharField(max_length=30, blank=True, null=True)

    # Optional first name field, can be left blank or set to null.
    first_name = models.CharField(max_length=30, blank=True, null=True)

    # Boolean flags for account status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Attach the custom manager
    objects = UserManager()

    # Set the USERNAME_FIELD to 'username' for login
    USERNAME_FIELD = "username"
    # Email and Phone number are required for user creation
    REQUIRED_FIELDS = [
        "email",
        "phone_number",
    ]

    # Timestamps for user creation and last update
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class for the UserModel.
        """

        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ("-created_at",)

    def __str__(self):
        """
        String representation of the user.
        """
        return self.username

    def get_full_name(self):
        """Returns the user's full name or an empty string if missing."""
        return " ".join(filter(None, [self.first_name, self.last_name])) or ""

    def clean(self):
        self.email = self.email.lower().strip()
        self.username = self.username.lower().strip()
        self.phone_number = self.phone_number.strip()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
