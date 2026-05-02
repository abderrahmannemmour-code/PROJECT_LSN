"""Serializers for the company internship offer API."""
from rest_framework import serializers
from core.models import InternshipOffer, OfferSkill
from student.models import Skill

ALGERIAN_WILAYAS = [
    ('01 - Adrar', '01 - Adrar'),
    ('02 - Chlef', '02 - Chlef'),
    ('03 - Laghouat', '03 - Laghouat'),
    ('04 - Oum El Bouaghi', '04 - Oum El Bouaghi'),
    ('05 - Batna', '05 - Batna'),
    ('06 - Béjaïa', '06 - Béjaïa'),
    ('07 - Biskra', '07 - Biskra'),
    ('08 - Béchar', '08 - Béchar'),
    ('09 - Blida', '09 - Blida'),
    ('10 - Bouira', '10 - Bouira'),
    ('11 - Tamanrasset', '11 - Tamanrasset'),
    ('12 - Tébessa', '12 - Tébessa'),
    ('13 - Tlemcen', '13 - Tlemcen'),
    ('14 - Tiaret', '14 - Tiaret'),
    ('15 - Tizi Ouzou', '15 - Tizi Ouzou'),
    ('16 - Alger', '16 - Alger'),
    ('17 - Djelfa', '17 - Djelfa'),
    ('18 - Jijel', '18 - Jijel'),
    ('19 - Sétif', '19 - Sétif'),
    ('20 - Saïda', '20 - Saïda'),
    ('21 - Skikda', '21 - Skikda'),
    ('22 - Sidi Bel Abbès', '22 - Sidi Bel Abbès'),
    ('23 - Annaba', '23 - Annaba'),
    ('24 - Guelma', '24 - Guelma'),
    ('25 - Constantine', '25 - Constantine'),
    ('26 - Médéa', '26 - Médéa'),
    ('27 - Mostaganem', '27 - Mostaganem'),
    ('28 - M\'Sila', '28 - M\'Sila'),
    ('29 - Mascara', '29 - Mascara'),
    ('30 - Ouargla', '30 - Ouargla'),
    ('31 - Oran', '31 - Oran'),
    ('32 - El Bayadh', '32 - El Bayadh'),
    ('33 - Illizi', '33 - Illizi'),
    ('34 - Bordj Bou Arréridj', '34 - Bordj Bou Arréridj'),
    ('35 - Boumerdès', '35 - Boumerdès'),
    ('36 - El Tarf', '36 - El Tarf'),
    ('37 - Tindouf', '37 - Tindouf'),
    ('38 - Tissemsilt', '38 - Tissemsilt'),
    ('39 - El Oued', '39 - El Oued'),
    ('40 - Khenchela', '40 - Khenchela'),
    ('41 - Souk Ahras', '41 - Souk Ahras'),
    ('42 - Tipaza', '42 - Tipaza'),
    ('43 - Mila', '43 - Mila'),
    ('44 - Aïn Defla', '44 - Aïn Defla'),
    ('45 - Naâma', '45 - Naâma'),
    ('46 - Aïn Témouchent', '46 - Aïn Témouchent'),
    ('47 - Ghardaïa', '47 - Ghardaïa'),
    ('48 - Relizane', '48 - Relizane'),
    ('49 - El M\'Ghair', '49 - El M\'Ghair'),
    ('50 - El Menia', '50 - El Menia'),
    ('51 - Ouled Djellal', '51 - Ouled Djellal'),
    ('52 - Bordj Badji Mokhtar', '52 - Bordj Badji Mokhtar'),
    ('53 - Béni Abbès', '53 - Béni Abbès'),
    ('54 - Timimoun', '54 - Timimoun'),
    ('55 - Touggourt', '55 - Touggourt'),
    ('56 - Djanet', '56 - Djanet'),
    ('57 - In Salah', '57 - In Salah'),
    ('58 - In Guezzam', '58 - In Guezzam'),
]

WILAYA_VALUES = [w[0] for w in ALGERIAN_WILAYAS]


class SkillSerializer(serializers.ModelSerializer):
    """Simple skill serializer for displaying required skills on offers."""
    class Meta:
        model = Skill
        fields = ['id', 'name']


class InternshipOfferSerializer(serializers.ModelSerializer):
    """
    Used for GET requests (list and detail).
    Shows all fields including computed duration and required skills.
    """
    duration_display = serializers.SerializerMethodField()
    company_name = serializers.CharField(
        source='company.name',
        read_only=True,
    )
    required_skills = serializers.SerializerMethodField()

    def get_duration_display(self, obj):
        return obj.duration_display

    def get_required_skills(self, obj):
        """
        Returns the list of required skills for this offer.
        We go through offer_skills (the junction table) and
        return the skill details for each one.
        """
        offer_skills = obj.offer_skills.select_related('skill').all()
        return SkillSerializer(
            [os.skill for os in offer_skills],
            many=True,
        ).data

    class Meta:
        model = InternshipOffer
        fields = [
            'id',
            'company',
            'company_name',
            'title',
            'description',
            'location',
            'wilaya',
            'type',
            'salary_per_week',
            'start_date',
            'end_date',
            'duration_display',
            'required_skills',
            'photo',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 'company', 'company_name',
            'duration_display', 'required_skills',
            'created_at', 'updated_at',
        ]


class CreateInternshipOfferSerializer(serializers.ModelSerializer):
    """
    Used for POST /api/company/offers/ (create).
    skill_ids is a list of skill IDs the company selects as required.
    Example: { "skill_ids": [1, 3, 7] }
    """
    skill_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=list,
        write_only=True,
        help_text='List of skill IDs required for this offer.',
    )
    wilaya = serializers.ChoiceField(
        choices=WILAYA_VALUES,
        required=True,
    )

    class Meta:
        model = InternshipOffer
        fields = [
            'title',
            'description',
            'location',
            'wilaya',
            'type',
            'salary_per_week',
            'start_date',
            'end_date',
            'photo',
            'status',
            'skill_ids',
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

    def validate_skill_ids(self, value):
        """Check all provided skill IDs actually exist."""
        if not value:
            return value
        existing = Skill.objects.filter(id__in=value)
        if existing.count() != len(set(value)):
            raise serializers.ValidationError(
                'One or more skill IDs are invalid.'
            )
        return value

    def validate_wilaya(self, value):
        """Ensure the wilaya is one of the 58 valid Algerian wilayas."""
        if value not in WILAYA_VALUES:
            raise serializers.ValidationError(
                'Invalid wilaya. Must be one of the 58 Algerian wilayas.'
            )
        return value

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

    def create(self, validated_data):
        """
        Pop skill_ids out before creating the offer
        (it's not a real DB field), then create the OfferSkill
        rows for each selected skill.
        """
        skill_ids = validated_data.pop('skill_ids', [])
        offer = InternshipOffer.objects.create(**validated_data)
        for skill_id in skill_ids:
            OfferSkill.objects.create(
                offer=offer,
                skill=Skill.objects.get(id=skill_id),
            )
        return offer


class UpdateInternshipOfferSerializer(serializers.ModelSerializer):
    """
    Used for PATCH /api/company/offers/<id>/ (partial update).
    Every field is optional. skill_ids replaces ALL current skills.
    Send [] to remove all skills, omit to keep existing ones unchanged.
    """
    skill_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True,
        help_text='Replaces all required skills. Send [] to clear all.',
    )
    wilaya = serializers.ChoiceField(
        choices=WILAYA_VALUES,
        required=False,
    )

    class Meta:
        model = InternshipOffer
        fields = [
            'title',
            'description',
            'location',
            'wilaya',
            'type',
            'salary_per_week',
            'start_date',
            'end_date',
            'photo',
            'status',
            'skill_ids',
        ]
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'location': {'required': False},
            'wilaya': {'required': False},
            'type': {'required': False},
            'salary_per_week': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False},
            'photo': {'required': False},
            'status': {'required': False},
        }

    def validate_skill_ids(self, value):
        if not value:
            return value
        existing = Skill.objects.filter(id__in=value)
        if existing.count() != len(set(value)):
            raise serializers.ValidationError(
                'One or more skill IDs are invalid.'
            )
        return value

    def validate(self, data):
        instance = self.instance
        start_date = data.get(
            'start_date', getattr(instance, 'start_date', None),
        )
        end_date = data.get(
            'end_date', getattr(instance, 'end_date', None),
        )
        offer_type = data.get(
            'type', getattr(instance, 'type', None),
        )
        salary = data.get(
            'salary_per_week', getattr(instance, 'salary_per_week', None),
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

    def update(self, instance, validated_data):
        """
        If skill_ids is present in the request, replace all
        existing skills with the new ones.
        If skill_ids is absent, leave skills untouched.
        """
        skill_ids = validated_data.pop('skill_ids', None)

        # Update all regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Only update skills if skill_ids was explicitly sent
        if skill_ids is not None:
            # Delete all existing required skills for this offer
            OfferSkill.objects.filter(offer=instance).delete()
            # Add the new ones
            for skill_id in skill_ids:
                OfferSkill.objects.create(
                    offer=instance,
                    skill=Skill.objects.get(id=skill_id),
                )

        return instance