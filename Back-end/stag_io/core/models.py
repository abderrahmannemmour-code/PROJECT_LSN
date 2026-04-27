"""Database models."""
import os
import uuid

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


def agreement_file_path(instance, filename):
    """Generate file path for internship agreement PDF."""
    filename = f'{uuid.uuid4()}.pdf'
    return os.path.join('uploads', 'agreements', filename)


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

    university = models.ForeignKey(
        University, on_delete=models.CASCADE,
        related_name='students', null=True, blank=True,
    )
    full_name = models.CharField(max_length=255)
    wilaya = models.CharField(max_length=100)
    github_link = models.URLField(max_length=255, blank=True)
    portfolio_link = models.URLField(max_length=255, blank=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to=profile_image_file_path,
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
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
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
    


class InternshipOffer(models.Model):
    """
    An internship offer posted by a Company.
    Students will browse and apply to these offers.
    """

    class Type(models.TextChoices):
        PAID = 'paid', 'Paid'
        UNPAID = 'unpaid', 'Unpaid'

    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='offers',
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.UNPAID,
    )
    salary_per_week = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    photo = models.ImageField(
        null=True,
        blank=True,
        upload_to='uploads/offer_photos/',
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Internship Offer'
        verbose_name_plural = 'Internship Offers'

    def __str__(self):
        return f'{self.title} — {self.company.name}'

    @property
    def duration_display(self):
        """
        Human-readable duration with sensible rounding.
        - Within 5 days of a month → 'X months'
        - Within 3 days of a week  → 'X weeks'
        - Otherwise                → 'X days'
        """
        delta = (self.end_date - self.start_date).days
        if delta <= 0:
            return 'Invalid dates'

        months = round(delta / 30)
        if months >= 1 and abs(delta - months * 30) <= 5:
            return f'{months} month{"s" if months > 1 else ""}'

        weeks = round(delta / 7)
        if weeks >= 1 and abs(delta - weeks * 7) <= 3:
            return f'{weeks} week{"s" if weeks > 1 else ""}'

        return f'{delta} day{"s" if delta > 1 else ""}'


class Notification(models.Model):
    """Notification sent to an admin when an internship needs attention."""

    class Type(models.TextChoices):
        INTERNSHIP_ACCEPTED = 'internship_accepted', 'Internship Accepted by Company'
        INTERNSHIP_VALIDATED = 'internship_validated', 'Internship Validated'
        INTERNSHIP_REJECTED = 'internship_rejected', 'Internship Rejected'

    recipient = models.ForeignKey(
        Admin, on_delete=models.CASCADE, related_name='notifications',
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
