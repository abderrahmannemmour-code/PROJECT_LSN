"""Database models."""
import os
import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def logo_image_file_path(instance, filename):
    """Generate file path for new logo image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'logo', filename)


def profile_image_file_path(instance, filename):
    """Generate file path for new student profile image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'profile', filename)


def university_logo_file_path(instance, filename):
    """Generate file path for new university logo image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'university', filename)


def offer_image_file_path(instance, filename):
    """Generate file path for new offer image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'offers', filename)


def agreement_file_path(instance, filename):
    """Generate file path for internship agreement PDF."""
    filename = f'{uuid.uuid4()}.pdf'
    return os.path.join('uploads', 'agreements', filename)


class Skill(models.Model):
    """Available skills for students to choose from."""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class University(models.Model):
    """Represents a university institution."""
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    wilaya = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    logo = models.ImageField(
        null=True, blank=True, upload_to=university_logo_file_path,
    )

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        return self.name


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
        extra_fields.setdefault('role', User.Roles.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Base user model for the platform."""

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


class Student(User):
    """Student user — inherits all User fields directly."""

    class InternshipPrivacy(models.TextChoices):
        PUBLIC   = 'public',   'Public — everyone can see'
        PRIVATE  = 'private',  'Private — only me'
        SELECTED = 'selected', 'Selected — I choose which ones'

    class AcademicYear(models.TextChoices):
        YEAR_1 = '1', '1st Year (L1)'
        YEAR_2 = '2', '2nd Year (L2)'
        YEAR_3 = '3', '3rd Year (L3)'
        YEAR_4 = '4', '4th Year (M1)'
        YEAR_5 = '5', '5th Year (M2)'
        DOCTORATE = 'D', 'Doctorate'

    university = models.ForeignKey(
        University, on_delete=models.CASCADE,
        related_name='students', null=True, blank=True,
    )
    academic_year = models.CharField(
        max_length=2,
        choices=AcademicYear.choices,
        default=AcademicYear.YEAR_3,
    )
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    wilaya = models.CharField(max_length=100)
    bio = models.TextField(blank=True, default='')
    github_link = models.URLField(max_length=255, blank=True)
    portfolio_link = models.URLField(max_length=255, blank=True)
    skills = models.ManyToManyField(
        Skill, related_name='students', blank=True,
    )
    profile_image = models.ImageField(
        null=True, blank=True, upload_to=profile_image_file_path,
    )
    last_seen = models.DateTimeField(null=True, blank=True)
    internship_privacy = models.CharField(
        max_length=20,
        choices=InternshipPrivacy.choices,
        default=InternshipPrivacy.PRIVATE,
    )

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def save(self, *args, **kwargs):
        self.role = User.Roles.STUDENT
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class Company(User):
    """Company user — inherits all User fields directly."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to=logo_image_file_path)
    wilaya = models.CharField(max_length=100)
    website = models.URLField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    industry = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def save(self, *args, **kwargs):
        self.role = User.Roles.COMPANY
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Admin(User):
    """Admin user — inherits all User fields directly."""

    university = models.ForeignKey(
        University, on_delete=models.CASCADE,
        related_name='admins', null=True, blank=True,
    )
    department = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def save(self, *args, **kwargs):
        self.role = User.Roles.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.email}'


class InternshipOffer(models.Model):
    """A specific internship posting by a company."""

    class OfferType(models.TextChoices):
        PAID = 'paid', 'Paid'
        UNPAID = 'unpaid', 'Unpaid'

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='offers',
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    type = models.CharField(
        max_length=20,
        choices=OfferType.choices,
        default=OfferType.UNPAID,
    )
    salary = models.IntegerField(null=True, blank=True)
    requirements = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, related_name='offers', blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    image = models.ImageField(
        null=True, blank=True, upload_to=offer_image_file_path,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} @ {self.company.name}'


class Internship(models.Model):
    """Represents an internship linking a Student to a Company."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED_BY_COMPANY = 'accepted_by_company', 'Accepted by Company'
        VALIDATED = 'validated', 'Validated'
        REJECTED = 'rejected', 'Rejected'

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='internships',
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='internships',
    )
    offer = models.ForeignKey(
        'InternshipOffer', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='applications',
    )
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Internship'
        verbose_name_plural = 'Internships'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student.full_name} @ {self.company.name} — {self.status}'


class InternshipAgreement(models.Model):
    """Stores the generated Convention de Stage PDF for an internship."""
    internship = models.OneToOneField(
        Internship, on_delete=models.CASCADE, related_name='agreement',
    )
    pdf_file = models.FileField(upload_to=agreement_file_path)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Internship Agreement'
        verbose_name_plural = 'Internship Agreements'

    def __str__(self):
        return f'Agreement for {self.internship}'


class Notification(models.Model):
    """Notification sent to an admin when an internship needs attention."""

    class Type(models.TextChoices):
        NEW_APPLICATION = 'new_application', 'New Application'
        INTERNSHIP_ACCEPTED = 'internship_accepted', 'Internship Accepted by Company'
        INTERNSHIP_VALIDATED = 'internship_validated', 'Internship Validated'
        INTERNSHIP_REJECTED = 'internship_rejected', 'Internship Rejected'

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications',
    )
    internship = models.ForeignKey(
        Internship, on_delete=models.CASCADE, related_name='notifications',
    )
    notification_type = models.CharField(
        max_length=30,
        choices=Type.choices,
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.notification_type} → {self.recipient.email}'


class StudentNotification(models.Model):
    """Notification sent to a student about their internship status."""

    class Type(models.TextChoices):
        INTERNSHIP_VALIDATED = 'internship_validated', 'Internship Validated by University'
        INTERNSHIP_REJECTED = 'internship_rejected', 'Internship Rejected by University'
        AGREEMENT_READY = 'agreement_ready', 'Convention de Stage Ready'

    recipient = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_notifications',
    )
    internship = models.ForeignKey(
        Internship, on_delete=models.CASCADE, related_name='student_notifications',
    )
    notification_type = models.CharField(
        max_length=30,
        choices=Type.choices,
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Student Notification'
        verbose_name_plural = 'Student Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.notification_type} → {self.recipient.email}'


class CompanyNotification(models.Model):
    """Notification sent to a company when an internship needs attention."""

    class Type(models.TextChoices):
        NEW_APPLICATION = 'new_application', 'New Internship Application'
        APPLICATION_VALIDATED = 'application_validated', 'Internship Validated by Admin'
        APPLICATION_REJECTED = 'application_rejected', 'Internship Rejected by Admin'

    recipient = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='company_notifications',
    )
    internship = models.ForeignKey(
        Internship, on_delete=models.CASCADE, related_name='company_notifications',
    )
    notification_type = models.CharField(
        max_length=30,
        choices=Type.choices,
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Company Notification'
        verbose_name_plural = 'Company Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.notification_type} → {self.recipient.email}'
