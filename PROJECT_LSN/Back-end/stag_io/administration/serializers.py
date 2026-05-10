"""Serializers for the administration API."""
from rest_framework import serializers

from core.models import (
    Internship, InternshipAgreement, Notification,
    Company, InternshipOffer, StudentNotification,
    CompanyNotification,
)


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
    student_image = serializers.ImageField(
        source='student.profile_image', read_only=True,
    )
    location = serializers.CharField(
        source='company.wilaya', read_only=True,
    )
    offer_title = serializers.SerializerMethodField()
    offer_duration = serializers.SerializerMethodField()

    class Meta:
        model = Internship
        fields = [
            'id',
            'student',
            'student_name',
            'student_email',
            'student_image',
            'company',
            'company_name',
            'company_email',
            'location',
            'offer_title',
            'offer_duration',
            'subject',
            'description',
            'start_date',
            'end_date',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_offer_title(self, obj):
        if obj.offer:
            return obj.offer.title
        return obj.subject

    def get_offer_duration(self, obj):
        if obj.offer:
            if obj.offer.start_date and obj.offer.end_date:
                return f"{obj.offer.start_date} to {obj.offer.end_date}"
        return None


class AdminInternshipDetailSerializer(AdminInternshipSerializer):
    """Detailed internship serializer with agreement + full student/company."""
    agreement = InternshipAgreementSerializer(read_only=True)
    student_details = serializers.SerializerMethodField()
    company_details = serializers.SerializerMethodField()
    offer_details = serializers.SerializerMethodField()

    class Meta(AdminInternshipSerializer.Meta):
        fields = AdminInternshipSerializer.Meta.fields + [
            'agreement', 'student_details', 'company_details', 'offer_details',
        ]

    def get_student_details(self, obj):
        from user.serializers import StudentUpdateSerializer
        return StudentUpdateSerializer(obj.student).data

    def get_company_details(self, obj):
        return CompanyPublicSerializer(obj.company).data

    def get_offer_details(self, obj):
        if obj.offer:
            return InternshipOfferSerializer(obj.offer).data
        return None


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


class StudentNotificationSerializer(serializers.ModelSerializer):
    """Serializer for student notifications."""
    internship_id = serializers.IntegerField(
        source='internship.id', read_only=True,
    )
    internship_subject = serializers.SerializerMethodField()
    company_name = serializers.CharField(
        source='internship.company.name', read_only=True,
    )
    has_agreement = serializers.SerializerMethodField()

    class Meta:
        model = StudentNotification
        fields = [
            'id',
            'internship_id',
            'notification_type',
            'message',
            'internship_subject',
            'company_name',
            'has_agreement',
            'is_read',
            'created_at',
        ]
        read_only_fields = fields

    def get_internship_subject(self, obj):
        if obj.internship.offer:
            return obj.internship.offer.title
        return obj.internship.subject

    def get_has_agreement(self, obj):
        return hasattr(obj.internship, 'agreement') and bool(
            obj.internship.agreement.pdf_file
        )


class CompanyNotificationSerializer(serializers.ModelSerializer):
    """Serializer for company notifications."""
    internship_id = serializers.IntegerField(
        source='internship.id', read_only=True,
    )
    internship_subject = serializers.SerializerMethodField()
    student_name = serializers.CharField(
        source='internship.student.full_name', read_only=True,
    )

    class Meta:
        model = CompanyNotification
        fields = [
            'id',
            'internship_id',
            'notification_type',
            'message',
            'internship_subject',
            'student_name',
            'is_read',
            'created_at',
        ]
        read_only_fields = fields

    def get_internship_subject(self, obj):
        if obj.internship.offer:
            return obj.internship.offer.title
        return obj.internship.subject


class InternshipApplySerializer(serializers.ModelSerializer):
    """Serializer for students to apply for an internship via an offer."""
    offer_id = serializers.IntegerField(write_only=True, required=False)
    offer_title = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    company_logo = serializers.SerializerMethodField()
    offer_duration = serializers.SerializerMethodField()
    offer_skills = serializers.SerializerMethodField()

    class Meta:
        model = Internship
        fields = [
            'id', 'company', 'offer_id', 'offer_title', 'company_name',
            'company_logo', 'offer_duration', 'offer_skills',
            'subject', 'description', 'start_date', 'end_date', 'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'company', 'subject', 'description', 'created_at']

    def get_offer_title(self, obj):
        if obj.offer:
            return obj.offer.title
        return obj.subject

    def get_company_name(self, obj):
        return obj.company.name if obj.company else None

    def get_company_logo(self, obj):
        if obj.company and obj.company.logo:
            return obj.company.logo.url
        return None

    def get_offer_duration(self, obj):
        if obj.offer and obj.offer.start_date and obj.offer.end_date:
            return f"{obj.offer.start_date} to {obj.offer.end_date}"
        return None

    def get_offer_skills(self, obj):
        if obj.offer:
            from user.serializers import SkillSerializer
            return SkillSerializer(obj.offer.skills.all(), many=True).data
        return []

    def create(self, validated_data):
        """Create a new internship for the authenticated student."""
        from core.models import Student, InternshipOffer
        user = self.context['request'].user
        student = Student.objects.get(pk=user.pk)
        offer_id = validated_data.pop('offer_id', None)

        if offer_id:
            offer = InternshipOffer.objects.get(pk=offer_id)
            validated_data['offer'] = offer
            validated_data['company'] = offer.company
            validated_data['subject'] = offer.title
            if not validated_data.get('description'):
                validated_data['description'] = offer.description or ''

        validated_data['student'] = student
        validated_data['status'] = Internship.Status.PENDING
        return super().create(validated_data)


class CompanyInternshipSerializer(serializers.ModelSerializer):
    """Serializer for companies to manage internship requests."""
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_email = serializers.EmailField(source='student.email', read_only=True)
    student_image = serializers.ImageField(source='student.profile_image', read_only=True)
    offer_title = serializers.SerializerMethodField()
    offer_id = serializers.IntegerField(source='offer.id', read_only=True)
    student_details = serializers.SerializerMethodField()

    class Meta:
        model = Internship
        fields = [
            'id', 'student', 'student_name', 'student_email', 'student_image',
            'student_details', 'offer_id', 'offer_title', 'subject', 'description',
            'start_date', 'end_date', 'status', 'created_at',
        ]
        read_only_fields = fields

    def get_offer_title(self, obj):
        if obj.offer:
            return obj.offer.title
        return obj.subject

    def get_student_details(self, obj):
        """Returns the full student profile (Digital CV)."""
        from user.serializers import StudentUpdateSerializer
        return StudentUpdateSerializer(obj.student).data


class CompanyPublicSerializer(serializers.ModelSerializer):
    """Public serializer for companies listed on the landing page."""

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'wilaya', 'website', 'logo', 'phone_number', 'industry']


class InternshipOfferSerializer(serializers.ModelSerializer):
    """Serializer for specific internship offers."""
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_logo = serializers.ImageField(source='company.logo', read_only=True)
    company_details = serializers.SerializerMethodField()
    wilaya = serializers.CharField(source='location', read_only=True)
    skills_details = serializers.SerializerMethodField()
    already_applied = serializers.SerializerMethodField()

    class Meta:
        model = InternshipOffer
        fields = [
            'id', 'company', 'company_name', 'company_logo', 'company_details',
            'title', 'description', 'location', 'wilaya', 'type', 'salary', 'requirements',
            'skills', 'skills_details', 'start_date', 'end_date',
            'image', 'is_active', 'created_at', 'already_applied',
        ]
        read_only_fields = ['id', 'company', 'created_at']

    def get_skills_details(self, obj):
        """Returns full skill objects."""
        from user.serializers import SkillSerializer
        return SkillSerializer(obj.skills.all(), many=True).data

    def get_company_details(self, obj):
        return CompanyPublicSerializer(obj.company).data

    def get_already_applied(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        if getattr(request.user, 'role', '') != 'student':
            return False
        return obj.applications.filter(student__pk=request.user.pk).exists()


class CompanyOfferStatsSerializer(serializers.Serializer):
    """Statistics for a single offer."""
    offer_id = serializers.IntegerField()
    offer_title = serializers.CharField()
    total = serializers.IntegerField()
    pending = serializers.IntegerField()
    accepted = serializers.IntegerField()
    rejected = serializers.IntegerField()
    validated = serializers.IntegerField()
