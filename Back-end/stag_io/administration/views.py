"""Views for the administration API."""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from core.models import Admin, Internship
from administration.serializers import AdminInternshipSerializer
from administration.permissions import IsAdminUser, IsAdminOfSameUniversity


@extend_schema(tags=['Administration'])
class PendingInternshipListView(generics.ListAPIView):
    """List internships awaiting admin validation (scoped to university)."""
    serializer_class = AdminInternshipSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        admin = Admin.objects.get(pk=self.request.user.pk)
        return Internship.objects.filter(
            student__university=admin.university,
            status=Internship.Status.ACCEPTED_BY_COMPANY,
        ).select_related('student', 'company')


@extend_schema(tags=['Administration'])
class AllInternshipListView(generics.ListAPIView):
    """List all internships for admin's university."""
    serializer_class = AdminInternshipSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        admin = Admin.objects.get(pk=self.request.user.pk)
        return Internship.objects.filter(
            student__university=admin.university,
        ).select_related('student', 'company')


@extend_schema(tags=['Administration'])
class InternshipDetailView(generics.RetrieveAPIView):
    """Retrieve a single internship detail."""
    serializer_class = AdminInternshipSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsAdminOfSameUniversity]

    def get_queryset(self):
        return Internship.objects.select_related('student', 'company')


@extend_schema(tags=['Administration'])
class ValidateInternshipView(APIView):
    """Validate an internship (set status to 'validated')."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsAdminOfSameUniversity]

    def patch(self, request, pk):
        try:
            internship = Internship.objects.select_related(
                'student', 'company',
            ).get(pk=pk)
        except Internship.DoesNotExist:
            return Response(
                {'detail': 'Internship not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check university scope
        admin = Admin.objects.get(pk=request.user.pk)
        if internship.student.university != admin.university:
            return Response(
                {'detail': 'Not allowed.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if internship.status != Internship.Status.ACCEPTED_BY_COMPANY:
            return Response(
                {'detail': 'Only internships accepted by a company can be validated.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        internship.status = Internship.Status.VALIDATED
        internship.save()

        serializer = AdminInternshipSerializer(internship)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Administration'])
class RejectInternshipView(APIView):
    """Reject an internship (set status to 'rejected')."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsAdminOfSameUniversity]

    def patch(self, request, pk):
        try:
            internship = Internship.objects.select_related(
                'student', 'company',
            ).get(pk=pk)
        except Internship.DoesNotExist:
            return Response(
                {'detail': 'Internship not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check university scope
        admin = Admin.objects.get(pk=request.user.pk)
        if internship.student.university != admin.university:
            return Response(
                {'detail': 'Not allowed.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if internship.status not in [
            Internship.Status.PENDING,
            Internship.Status.ACCEPTED_BY_COMPANY,
        ]:
            return Response(
                {'detail': 'This internship cannot be rejected.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        internship.status = Internship.Status.REJECTED
        internship.save()

        serializer = AdminInternshipSerializer(internship)
        return Response(serializer.data, status=status.HTTP_200_OK)

