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
