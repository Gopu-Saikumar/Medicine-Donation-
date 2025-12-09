from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# ----------------------------
# Custom User Manager
# ----------------------------

class UserManager(BaseUserManager):
    def create_user(self, email, fullname, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            fullname=fullname,
            phone=phone,
        )

        user.set_password(password)  # securely hashes password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, phone, password):
        user = self.create_user(email, fullname, phone, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# ----------------------------
# Custom User Model
# ----------------------------

class User(AbstractBaseUser):
    fullname = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    # Authentication flags
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.fullname

    @property
    def is_staff(self):
        return self.is_admin



