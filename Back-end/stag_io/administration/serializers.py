"""Serializers for the administration API."""
from rest_framework import serializers

from core.models import Internship, Notification


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


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for admin notifications."""
    internship_id = serializers.IntegerField(
        source='internship.id', read_only=True,
    )
    student_name = serializers.CharField(
        source='internship.student.full_name', read_only=True,
    )
    company_name = serializers.CharField(
        source='internship.company.name', read_only=True,
    )
    internship_subject = serializers.CharField(
        source='internship.subject', read_only=True,
    )
    internship_status = serializers.CharField(
        source='internship.status', read_only=True,
    )

    class Meta:
        model = Notification
        fields = [
            'id',
            'internship_id',
            'notification_type',
            'message',
            'student_name',
            'company_name',
            'internship_subject',
            'internship_status',
            'is_read',
            'created_at',
        ]
        read_only_fields = [
            'id', 'notification_type', 'message', 'created_at',
        ]
