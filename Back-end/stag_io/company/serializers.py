"""Serializers for the company internship offer API."""
from rest_framework import serializers
from core.models import InternshipOffer


class InternshipOfferSerializer(serializers.ModelSerializer):
    duration_display = serializers.SerializerMethodField()
    company_name = serializers.CharField(
        source='company.name',
        read_only=True,
    )

    def get_duration_display(self, obj):
        """
        Calls the duration_display property on the model.
        obj is the InternshipOffer instance being serialized.
        """
        return obj.duration_display

    class Meta:
        model = InternshipOffer
        fields = [
            'id',
            'company',
            'company_name',
            'title',
            'description',
            'location',
            'type',
            'salary_per_week',
            'start_date',
            'end_date',
            'duration_display',
            'photo',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 'company', 'company_name',
            'duration_display', 'created_at', 'updated_at',
        ]

class CreateInternshipOfferSerializer(serializers.ModelSerializer):
    """
    Used for POST /api/company/offers/ (create).
    All required fields must be provided.
    """
    class Meta:
        model = InternshipOffer
        fields = [
            'title',
            'description',
            'location',
            'type',
            'salary_per_week',
            'start_date',
            'end_date',
            'photo',
            'status',
        ]
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'location': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'type': {'required': True},
            'salary_per_week': {'required': False},
            'photo': {'required': False},
            'status': {'required': False},
        }

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        offer_type = data.get('type')
        salary = data.get('salary_per_week')

        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError(
                    'End date must be after start date.'
                )
            delta = (end_date - start_date).days
            if delta < 14:
                raise serializers.ValidationError(
                    'Internship must be at least 2 weeks (14 days).'
                )

        if offer_type == InternshipOffer.Type.PAID:
            if not salary:
                raise serializers.ValidationError(
                    'salary_per_week is required for paid internships.'
                )
            if salary <= 0:
                raise serializers.ValidationError(
                    'salary_per_week must be a positive number.'
                )

        if offer_type == InternshipOffer.Type.UNPAID:
            data['salary_per_week'] = None

        return data


class UpdateInternshipOfferSerializer(serializers.ModelSerializer):
    """
    Used for PATCH /api/company/offers/<id>/ (partial update).
    Every field is optional — only send what you want to change.
    Same validation rules apply.
    """
    class Meta:
        model = InternshipOffer
        fields = [
            'title',
            'description',
            'location',
            'type',
            'salary_per_week',
            'start_date',
            'end_date',
            'photo',
            'status',
        ]
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'location': {'required': False},
            'type': {'required': False},
            'salary_per_week': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False},
            'photo': {'required': False},
            'status': {'required': False},
        }

    def validate(self, data):
        # Fall back to existing instance values for fields not being updated
        instance = self.instance
        start_date = data.get(
            'start_date',
            getattr(instance, 'start_date', None),
        )
        end_date = data.get(
            'end_date',
            getattr(instance, 'end_date', None),
        )
        offer_type = data.get(
            'type',
            getattr(instance, 'type', None),
        )
        salary = data.get(
            'salary_per_week',
            getattr(instance, 'salary_per_week', None),
        )

        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError(
                    'End date must be after start date.'
                )
            delta = (end_date - start_date).days
            if delta < 14:
                raise serializers.ValidationError(
                    'Internship must be at least 2 weeks (14 days).'
                )

        if offer_type == InternshipOffer.Type.PAID:
            if not salary:
                raise serializers.ValidationError(
                    'salary_per_week is required for paid internships.'
                )
            if salary <= 0:
                raise serializers.ValidationError(
                    'salary_per_week must be a positive number.'
                )

        if offer_type == InternshipOffer.Type.UNPAID:
            data['salary_per_week'] = None

        return data