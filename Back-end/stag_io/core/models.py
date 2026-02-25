"""Database models."""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a Django superuser (system administrator)."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', self.model.Roles.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def create_student(self, email, password, full_name, wilaya, **extra_fields):
        """Create a user with role='student' and a Student profile."""
        extra_fields['role'] = 'student'
        user = self.create_user(email, password, **extra_fields)
        Student.objects.create(
            user=user,
            full_name=full_name,
            wilaya=wilaya,
        )
        return user

    def create_company(self, email, password, name, wilaya, **extra_fields):
        """Create a user with role='company' and a Company profile."""
        extra_fields['role'] = 'company'
        user = self.create_user(email, password, **extra_fields)
        Company.objects.create(
            user=user,
            name=name,
            wilaya=wilaya,
        )
        return user

    def create_admin(self, email, password, department, title, **extra_fields):
        """Create a user with role='admin' and an AdminProfile."""
        extra_fields['role'] = 'admin'
        user = self.create_user(email, password, **extra_fields)
        Admin.objects.create(
            user=user,
            department=department,
            title=title,
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for the platform."""

    class Roles(models.TextChoices):
        STUDENT = 'student', 'Student'
        COMPANY = 'company', 'Company'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Student(models.Model):
    """Student profile linked to a user account."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
    )
    full_name = models.CharField(max_length=255)
    wilaya = models.CharField(max_length=100)
    github_link = models.URLField(max_length=255, blank=True)
    portfolio_link = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.full_name


class Company(models.Model):
    """Company profile linked to a user account."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company_profile',
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    wilaya = models.CharField(max_length=100)
    website = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Admin(models.Model):
    """Admin profile linked to a user account."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_profile',
    )
    department = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} - {self.user.email}'
