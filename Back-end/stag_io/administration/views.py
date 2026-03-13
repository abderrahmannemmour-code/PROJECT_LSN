"""Views for the administration API."""
from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from core.models import Admin, Internship, Notification
from administration.serializers import (
    AdminInternshipDetailSerializer,
    AdminInternshipSerializer,
    NotificationSerializer,
)
from administration.permissions import IsAdminUser, IsAdminOfSameUniversity
from administration.services import generate_internship_agreement


# ── Notification views ──────────────────────────────────────────────

@extend_schema(tags=['Administration - Notifications'])
class NotificationListView(generics.ListAPIView):
    """List all notifications for the authenticated admin."""
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient__pk=self.request.user.pk,
        ).select_related(
            'internship', 'internship__student', 'internship__company',
        )


@extend_schema(tags=['Administration - Notifications'])
class UnreadNotificationListView(generics.ListAPIView):
    """List unread notifications for the authenticated admin."""
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient__pk=self.request.user.pk,
            is_read=False,
        ).select_related(
            'internship', 'internship__student', 'internship__company',
        )


@extend_schema(tags=['Administration - Notifications'])
class MarkNotificationReadView(APIView):
    """Mark a single notification as read."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(
                pk=pk, recipient__pk=request.user.pk,
            )
        except Notification.DoesNotExist:
            return Response(
                {'detail': 'Notification not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        notification.is_read = True
        notification.save()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ── Internship views ────────────────────────────────────────────────


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
    serializer_class = AdminInternshipDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsAdminOfSameUniversity]

    def get_queryset(self):
        return Internship.objects.select_related(
            'student', 'student__university', 'company', 'agreement',
        )


@extend_schema(tags=['Administration'])
class DownloadInternshipAgreementView(APIView):
    """Download the generated internship agreement PDF."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsAdminOfSameUniversity]

    def get(self, request, pk):
        try:
            internship = Internship.objects.select_related(
                'student', 'student__university', 'company', 'agreement',
            ).get(pk=pk)
        except Internship.DoesNotExist:
            return Response(
                {'detail': 'Internship not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        admin = Admin.objects.get(pk=request.user.pk)
        if internship.student.university != admin.university:
            return Response(
                {'detail': 'Not allowed.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not hasattr(internship, 'agreement') or not internship.agreement.pdf_file:
            return Response(
                {'detail': 'Agreement not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        internship.agreement.pdf_file.open('rb')
        return FileResponse(
            internship.agreement.pdf_file,
            as_attachment=True,
            filename=f'internship_agreement_{internship.id}.pdf',
            content_type='application/pdf',
        )


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

        try:
            generate_internship_agreement(internship, admin=admin)
        except ValueError as error:
            internship.status = Internship.Status.ACCEPTED_BY_COMPANY
            internship.save(update_fields=['status'])
            return Response(
                {'detail': str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mark related notifications as read
        Notification.objects.filter(
            internship=internship,
            recipient__pk=request.user.pk,
        ).update(is_read=True)

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

        # Mark related notifications as read
        Notification.objects.filter(
            internship=internship,
            recipient__pk=request.user.pk,
        ).update(is_read=True)

        serializer = AdminInternshipSerializer(internship)
        return Response(serializer.data, status=status.HTTP_200_OK)

