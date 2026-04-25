"""Views for the student skills API."""
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.openapi import AutoSchema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Student
from student.models import Skill, StudentSkill
from student.serializers import (
    SkillSerializer,
    StudentSkillSerializer,
    AddStudentSkillSerializer,
)
from user.views import IsStudent


def get_student(request):
    """Get the Student object for the currently logged-in user."""
    return Student.objects.get(pk=request.user.pk)


@extend_schema(tags=['Skills'])
class SkillListView(generics.ListAPIView):
    """
    GET /api/student/skills/
    Returns all available skills as a flat list.
    Used to populate the chips selector on the profile page.
    Any authenticated user can call this.
    """
    serializer_class = SkillSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Skill.objects.all()


@extend_schema(tags=['Skills'])
class MySkillListView(generics.ListAPIView):
    """
    GET /api/student/me/skills/
    Returns the skills the logged-in student has selected.
    These are the chips currently shown on their profile.
    """
    serializer_class = StudentSkillSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]

    def get_queryset(self):
        student = get_student(self.request)
        return StudentSkill.objects.filter(
            student=student,
        ).select_related('skill')


@extend_schema(
    tags=['Skills'],
    request=AddStudentSkillSerializer,
    responses={201: StudentSkillSerializer},
)
class AddSkillView(APIView):
    """
    POST /api/student/me/skills/add/
    Student adds a skill chip to their profile.
    Request body: { "skill_id": 3 }
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]

    def post(self, request):
        serializer = AddStudentSkillSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        skill_id = serializer.validated_data['skill_id']
        student = get_student(request)
        skill = Skill.objects.get(id=skill_id)

        if StudentSkill.objects.filter(student=student, skill=skill).exists():
            return Response(
                {'detail': 'You already have this skill.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        student_skill = StudentSkill.objects.create(
            student=student,
            skill=skill,
        )

        return Response(
            StudentSkillSerializer(student_skill).data,
            status=status.HTTP_201_CREATED,
        )

@extend_schema(tags=['Skills'])
class RemoveSkillView(APIView):
    """
    DELETE /api/student/me/skills/<id>/remove/
    Student removes a skill chip by clicking X.
    The <id> is the StudentSkill ID from GET /me/skills/
    Returns 204 No Content on success.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]

    def delete(self, request, pk):
        student = get_student(request)

        try:
            student_skill = StudentSkill.objects.get(
                pk=pk,
                student=student,
            )
        except StudentSkill.DoesNotExist:
            return Response(
                {'detail': 'Skill not found on your profile.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        student_skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)