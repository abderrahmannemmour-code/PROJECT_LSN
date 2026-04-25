"""Serializers for the student skills API."""
from rest_framework import serializers
from student.models import Skill, StudentSkill


class SkillSerializer(serializers.ModelSerializer):
    """
    Converts a Skill to JSON.
    Example output: { "id": 1, "name": "React" }
    """
    class Meta:
        model = Skill
        fields = ['id', 'name']


class StudentSkillSerializer(serializers.ModelSerializer):
    """
    Converts a StudentSkill to JSON.
    Includes full skill details so the frontend can
    render the chip without a second API call.
    Example output: { "id": 5, "skill": { "id": 1, "name": "React" } }
    """
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = StudentSkill
        fields = ['id', 'skill']


class AddStudentSkillSerializer(serializers.Serializer):
    """
    Validates incoming data when a student adds a skill.
    Expects: { "skill_id": 1 }
    """
    skill_id = serializers.IntegerField()

    def validate_skill_id(self, value):
        """Check the skill actually exists."""
        if not Skill.objects.filter(id=value).exists():
            raise serializers.ValidationError('Skill not found.')
        return value