"""Serializers for the user API."""
from django.contrib.auth import get_user_model

from rest_framework import serializers

from core.models import Student, Company


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
            'github_link', 'portfolio_link',
        ]

    def validate_email(self, value):
        """Ensure the student registers with a university email."""
        allowed_domains = [
            'univ.dz',
            'edu.dz',
            'etu.univ.dz',
        ]
        domain = value.split('@')[-1].lower()
        if not any(domain == d or domain.endswith('.' + d) for d in allowed_domains):
            raise serializers.ValidationError(
                'Students must register with a university email '
                f'(e.g. name@univ.dz). Allowed domains: {", ".join(allowed_domains)}'
            )
        return value

    def create(self, validated_data):
        """Create and return a student with encrypted password."""
        password = validated_data.pop('password')
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
    """Serializer for updating student profile fields."""

    class Meta:
        model = Student
        fields = [
            'id', 'email',
            'full_name', 'wilaya',
            'bio',
            'github_link', 'portfolio_link',
            'profile_image',
            'last_seen',
            'internship_privacy',
        ]
        read_only_fields = ['id', 'email', 'profile_image', 'last_seen']
        extra_kwargs = {
            'full_name': {'required': False},
            'wilaya': {'required': False},
            'bio': {'required': False, 'allow_blank': True},
            'github_link': {'required': False, 'allow_blank': True},
            'portfolio_link': {'required': False, 'allow_blank': True},
            'internship_privacy': {'required': False},
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
