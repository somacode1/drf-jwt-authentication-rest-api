from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("username", email)
        
        if not extra_fields.get("role"):
            raise ValueError("User must have a role assigned.")

        if not email:
            raise ValueError("Users must have an email address")

        if self.model.objects.filter(email=email).exists():
            raise ValueError('User email already exists.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 'admin')

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Set email and password explicitly
        email = self.normalize_email(email)

        return self.create_user(email=email, password=password, **extra_fields)