"""Serializers for the administration API."""
from rest_framework import serializers
from core.models import Internship, InternshipAgreement, Notification


class InternshipAgreementSerializer(serializers.ModelSerializer):
    """Read-only serializer for internship agreement metadata."""
    pdf_url = serializers.FileField(source='pdf_file', read_only=True)

    class Meta:
        model = InternshipAgreement
        fields = ['id', 'pdf_url', 'generated_at']
        read_only_fields = fields


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


class AdminInternshipDetailSerializer(AdminInternshipSerializer):
    """Detailed internship serializer with agreement metadata."""
    agreement = InternshipAgreementSerializer(read_only=True)

    class Meta(AdminInternshipSerializer.Meta):
        fields = AdminInternshipSerializer.Meta.fields + ['agreement']


class NotificationSerializer(serializers.ModelSerializer):
    """Universal notification serializer for all actors."""
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
            'link',
            'student_name',
            'company_name',
            'internship_subject',
            'internship_status',
            'is_read',
            'created_at',
        ]
        read_only_fields = [
            'id', 'notification_type', 'message',
            'link', 'created_at',
        ]