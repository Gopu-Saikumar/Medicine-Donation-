from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ---------------------------
# USER MANAGER
# ---------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, fullname=None, phone=None, user_type="donor", password=None):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            fullname=fullname,
            phone=phone,
            user_type=user_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            user_type="admin"
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# ---------------------------
# USER MODEL
# ---------------------------
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ("donor", "Donor"),
        ("ngo", "NGO"),
        ("admin", "Admin"),
    )

    fullname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="donor")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


# ---------------------------
# NGO PROFILE MODEL
# ---------------------------
class NGOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="ngo_profile")
    ngo_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.ngo_name
