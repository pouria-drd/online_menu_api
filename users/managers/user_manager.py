from users.utils import normalize_phone
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for the UserModel, handling user and superuser creation.
    """

    def create_user(
        self,
        email=None,
        username=None,
        phone_number=None,
        password=None,
        **extra_fields
    ):
        """
        Creates and returns a regular user.
        """
        # Ensure that the user has an email
        if not email:
            raise ValueError("Users must have an email")

        # Ensure that the user has a username
        if not username:
            raise ValueError("Users must have a username")

        # Ensure that the user has a phone number
        if not phone_number:
            raise ValueError("Users must have a phone number")

        # Ensure that the user has a password
        if not password:
            raise ValueError("Users must have a password")

        # Convert username to lowercase for uniqueness
        username = username.lower()
        # Normalize phone number
        phone_number = normalize_phone(phone_number)
        # Normalize email
        email = self.normalize_email(email) if email else None

        # Create the user instance with the provided details
        user = self.model(
            email=email, username=username, phone_number=phone_number, **extra_fields
        )
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)  # Save the user to the database

        return user

    def create_superuser(
        self, email, username, phone_number, password=None, **extra_fields
    ):
        """
        Creates and returns a superuser with all permissions.
        """
        user = self.create_user(
            email=email,
            username=username,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )
        # Assign superuser status
        user.is_superuser = True
        # Allow admin panel access
        user.is_staff = True

        user.save(using=self._db)

        return user
