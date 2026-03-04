"""Serializers for the administration API."""
from rest_framework import serializers

from core.models import Internship


class AdminInternshipSerializer(serializers.ModelSerializer):
    """Read-only serializer for admin to review internships."""
    student_name = serializers.CharField(
        source='student.full_name', read_only=True,
    )
    company_name = serializers.CharField(
        source='company.name', read_only=True,
    )
    student_email = serializers.EmailField(
        source='student.email', read_only=True,
    )
    company_email = serializers.EmailField(
        source='company.email', read_only=True,
    )

    class Meta:
        model = Internship
        fields = [
            'id',
            'student',
            'student_name',
            'student_email',
            'company',
            'company_name',
            'company_email',
            'subject',
            'description',
            'start_date',
            'end_date',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
