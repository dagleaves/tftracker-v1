from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, password=None):
        """
        Creates and saves a User with the given first name, last name, 
        email,  and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have a username')

        email=self.normalize_email(email)
        email = email.lower()

        username = username.lower()

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

        
    def create_superuser(self, first_name, last_name, email, username, password=None):
        """
        Creates and saves a superuser with the given first name, 
        last name, email, and password.
        """
        user = self.create_user(
            first_name,
            last_name,
            email,
            username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.email

