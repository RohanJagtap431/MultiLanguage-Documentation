
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError("Mobile number is required")

        user = self.model(
            mobile_number=mobile_number,
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            mobile_number,
            password,
            **extra_fields
        )


class CustomUser(AbstractUser):

    username = None
    email = None

    name = models.CharField(max_length=100)

    mobile_number = models.CharField(
        max_length=15,
        unique=True
    )

    is_approved = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.mobile_number
