import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):

    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def createUser(self, email, username, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("Provide an email address")

        email=self.normalize_email(email)
        user=self.model(email=email, username=username, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.'")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_staff=True.'")

        return self.createUser(email, username, password, **extra_fields)

# Create a custom user model using AbstractBaseUser subclass

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    phone_number = PhoneNumberField(unique=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    
    objects = CustomUserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username', 'phone_number']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #display_photo = models.ImageField(upload_to="static/img/", default='avatar.jpeg' null=True, blank=True)
    bio_data = models.TextField()
    profile_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)


    def __str__(self):
        return self.name

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Blog(models.Model):
    title = models.CharField(max_length=200)
    blog_description = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now= True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title