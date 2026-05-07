"""Serializers for the user API."""
from django.contrib.auth import get_user_model

from rest_framework import serializers

from core.models import Student, Company, University, UNIVERSITY_EMAIL_DOMAINS


class StudentRegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering a new student."""
    password = serializers.CharField(
        write_only=True,
        min_length=5,
        style={'input_type': 'password'},
    )

    class Meta:
        model = Student
        fields = [
            'email', 'password',
            'full_name', 'wilaya',
        ]

    def validate_email(self, value):
        """
        Ensure the student registers with one of the 5 predefined
        university email domains. The university is auto-assigned.
        """
        domain = value.split('@')[-1].lower()
        if domain not in UNIVERSITY_EMAIL_DOMAINS:
            allowed = ', '.join(
                f'@{d}' for d in UNIVERSITY_EMAIL_DOMAINS.keys()
            )
            raise serializers.ValidationError(
                f'Students must register with a university email. '
                f'Allowed domains: {allowed}'
            )
        return value

    def create(self, validated_data):
        """Create and return a student with encrypted password.
        Automatically assigns the university based on email domain.
        """
        password = validated_data.pop('password')
        # Determine university from email domain
        email = validated_data['email']
        domain = email.split('@')[-1].lower()
        uni_code = UNIVERSITY_EMAIL_DOMAINS[domain]
        university = University.objects.get(code=uni_code)
        validated_data['university'] = university
        student = Student(**validated_data)
        student.set_password(password)
        student.save()
        return student


class CompanyRegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering a new company."""
    password = serializers.CharField(
        write_only=True,
        min_length=5,
        style={'input_type': 'password'},
    )

    class Meta:
        model = Company
        fields = [
            'email', 'password',
            'name', 'description',
            'wilaya', 'website',
        ]

    def create(self, validated_data):
        """Create and return a company with encrypted password."""
        password = validated_data.pop('password')
        company = Company(**validated_data)
        company.set_password(password)
        company.save()
        return company


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for the authenticated user detail (GET /me)."""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'role', 'is_active', 'created_at']
        read_only_fields = ['id', 'role', 'is_active', 'created_at']


class StudentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating student personal profile fields."""

    class Meta:
        model = Student
        fields = [
            'id', 'email',
            'full_name', 'wilaya',
            'date_of_birth',
        ]
        read_only_fields = ['id', 'email']
        extra_kwargs = {
            'full_name': {'required': False},
            'wilaya': {'required': False},
            'date_of_birth': {'required': False},
        }


class CompanyUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating company profile fields."""

    class Meta:
        model = Company
        fields = [
            'id', 'email',
            'name', 'description',
            'wilaya', 'website',
        ]
        read_only_fields = ['id', 'email']
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'wilaya': {'required': False},
            'website': {'required': False, 'allow_blank': True},
        }

class LogoImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to logos."""

    class Meta:
        model = Company
        fields = ['id', 'logo']
        read_only_fields = ['id']
        extra_kwargs = {
            'logo': {'required': True},
        }


class ProfileImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading student profile images."""

    class Meta:
        model = Student
        fields = ['id', 'profile_image']
        read_only_fields = ['id']
        extra_kwargs = {
            'profile_image': {'required': True},
        }
