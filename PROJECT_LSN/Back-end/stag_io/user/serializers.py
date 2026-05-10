"""Serializers for the user API."""
from django.contrib.auth import get_user_model

from rest_framework import serializers

from core.models import Student, Company, Skill, University


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
            'wilaya', 'website', 'phone_number'
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
    profile_image = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'role', 'is_active', 'created_at', 'profile_image', 'full_name']
        read_only_fields = ['id', 'role', 'is_active', 'created_at']

    def get_profile_image(self, obj):
        if obj.role == 'student':
            from core.models import Student
            try:
                student = Student.objects.get(pk=obj.pk)
                if student.profile_image:
                    return student.profile_image.url
            except Student.DoesNotExist:
                pass
        elif obj.role == 'company':
            from core.models import Company
            try:
                company = Company.objects.get(pk=obj.pk)
                if company.logo:
                    return company.logo.url
            except Company.DoesNotExist:
                pass
        return None

    def get_full_name(self, obj):
        if obj.role == 'student':
            from core.models import Student
            try:
                student = Student.objects.get(pk=obj.pk)
                return student.full_name or obj.email.split('@')[0]
            except Student.DoesNotExist:
                pass
        elif obj.role == 'company':
            from core.models import Company
            try:
                company = Company.objects.get(pk=obj.pk)
                return company.name or obj.email.split('@')[0]
            except Company.DoesNotExist:
                pass
        return obj.email.split('@')[0]


class UniversitySerializer(serializers.ModelSerializer):
    """Serializer for university objects."""

    class Meta:
        model = University
        fields = ['id', 'name', 'code', 'wilaya', 'logo']
        read_only_fields = ['id']


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for skill objects."""

    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']
        read_only_fields = ['id']


class StudentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating student profile fields."""
    skills = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skill.objects.all(),
        required=False
    )

    class Meta:
        model = Student
        fields = [
            'id', 'email',
            'full_name', 'birth_date', 'wilaya',
            'university', 'academic_year',
            'bio', 'skills',
            'github_link', 'portfolio_link',
            'profile_image',
            'last_seen',
            'internship_privacy',
        ]
        read_only_fields = ['id', 'email', 'profile_image', 'last_seen']
        extra_kwargs = {
            'full_name': {'required': False},
            'birth_date': {'required': False},
            'wilaya': {'required': False},
            'university': {'required': False},
            'academic_year': {'required': False},
            'bio': {'required': False, 'allow_blank': True},
            'github_link': {'required': False, 'allow_blank': True},
            'portfolio_link': {'required': False, 'allow_blank': True},
            'internship_privacy': {'required': False},
        }

    def to_representation(self, instance):
        """Show full skill and university objects in GET requests."""
        rep = super().to_representation(instance)
        rep['skills'] = SkillSerializer(instance.skills.all(), many=True).data
        if instance.university:
            rep['university'] = UniversitySerializer(instance.university).data
        return rep


class CompanyUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating company profile fields."""

    class Meta:
        model = Company
        fields = [
            'id', 'email',
            'name', 'description',
            'wilaya', 'website',
            'phone_number', 'industry',
        ]
        read_only_fields = ['id', 'email']
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'wilaya': {'required': False},
            'website': {'required': False, 'allow_blank': True},
            'phone_number': {'required': False, 'allow_blank': True},
            'industry': {'required': False, 'allow_blank': True},
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
