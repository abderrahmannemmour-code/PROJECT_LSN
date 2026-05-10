"""Views for the administration API."""
from datetime import timedelta

from django.http import FileResponse
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth, TruncWeek
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from administration.serializers import (
    AdminInternshipDetailSerializer,
    AdminInternshipSerializer,
    NotificationSerializer,
    InternshipApplySerializer,
    CompanyInternshipSerializer,
    CompanyPublicSerializer,
    InternshipOfferSerializer,
    StudentNotificationSerializer,
    CompanyOfferStatsSerializer,
    CompanyNotificationSerializer,
)
from administration.permissions import (
    IsAdminUser,
    IsAdminOfSameUniversity,
    IsStudentUser,
    IsCompanyUser,
)
from core.models import (
    Admin, Internship, Notification, Company, InternshipOffer,
    StudentNotification, CompanyNotification,
)
from administration.services import generate_internship_agreement


def _get_admin(request):
    """Return the authenticated admin object, or None if not found."""
    try:
        return Admin.objects.get(pk=request.user.pk)
    except Admin.DoesNotExist:
        return None


def _get_university_internships(request):
    """Return internships for the authenticated admin's university."""
    admin = _get_admin(request)
    if admin and admin.university:
        return Internship.objects.filter(student__university=admin.university)
    return Internship.objects.all()


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


@extend_schema(tags=['Administration - Notifications'])
class MarkAllNotificationsReadView(APIView):
    """Mark all notifications for the authenticated user as read."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        Notification.objects.filter(
            recipient__pk=request.user.pk,
            is_read=False,
        ).update(is_read=True)
        return Response(status=status.HTTP_200_OK)


# ── Internship views ────────────────────────────────────────────────


@extend_schema(tags=['Administration'])
class AllInternshipListView(generics.ListAPIView):
    """List all internships for admin's university."""
    serializer_class = AdminInternshipSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        admin = _get_admin(self.request)
        # Admin only sees internships that have moved past the initial company review
        allowed_statuses = ['accepted_by_company', 'validated', 'rejected_by_admin']
        
        if admin and admin.university:
            return Internship.objects.filter(
                student__university=admin.university,
                status__in=allowed_statuses
            ).select_related('student', 'company', 'offer')
        return Internship.objects.filter(
            status__in=allowed_statuses
        ).select_related('student', 'company', 'offer')


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

        admin = _get_admin(request)
        if admin and admin.university and internship.student.university != admin.university:
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
        admin = _get_admin(request)
        if admin and admin.university and internship.student.university != admin.university:
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

        # Mark related admin notifications as read
        Notification.objects.filter(
            internship=internship,
            recipient__pk=request.user.pk,
        ).update(is_read=True)

        # Notify the student that their internship is validated
        StudentNotification.objects.create(
            recipient=internship.student,
            internship=internship,
            notification_type=StudentNotification.Type.AGREEMENT_READY,
            message=(
                f'Your internship "{internship.offer.title if internship.offer else internship.subject}" '
                f'at {internship.company.name} has been validated. '
                f'Your Convention de Stage is ready to download.'
            ),
        )

        # Notify the company
        CompanyNotification.objects.create(
            recipient=internship.company,
            internship=internship,
            notification_type=CompanyNotification.Type.APPLICATION_VALIDATED,
            message=f'The internship application from {internship.student.full_name} has been validated by the university.',
        )

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
        admin = _get_admin(request)
        if admin and admin.university and internship.student.university != admin.university:
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

        # Mark related admin notifications as read
        Notification.objects.filter(
            internship=internship,
            recipient__pk=request.user.pk,
        ).update(is_read=True)

        # Notify the student
        StudentNotification.objects.create(
            recipient=internship.student,
            internship=internship,
            notification_type=StudentNotification.Type.INTERNSHIP_REJECTED,
            message=(
                f'Unfortunately, your internship "{internship.offer.title if internship.offer else internship.subject}" '
                f'at {internship.company.name} was not validated by the university.'
            ),
        )

        # Notify the company
        CompanyNotification.objects.create(
            recipient=internship.company,
            internship=internship,
            notification_type=CompanyNotification.Type.APPLICATION_REJECTED,
            message=f'The internship application from {internship.student.full_name} was rejected by the university.',
        )

        serializer = AdminInternshipSerializer(internship)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ── Statistics views ───────────────────────────────────────────────


@extend_schema(tags=['Administration - Statistics'])
class StatisticsSummaryView(APIView):
    """Main dashboard summary for admin's university."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        admin = _get_admin(request)
        from core.models import Student
        students_qs = admin.university.students.all() if admin and admin.university else Student.objects.all()
        internships_qs = _get_university_internships(request)

        total_students = students_qs.count()
        placed_students = students_qs.filter(
            internships__status__in=[
                Internship.Status.ACCEPTED_BY_COMPANY,
                Internship.Status.VALIDATED,
            ],
        ).distinct().count()
        unplaced_students = total_students - placed_students
        placement_rate = round(
            (placed_students / total_students) * 100, 2,
        ) if total_students else 0.0

        status_counts = internships_qs.aggregate(
            pending=Count('id', filter=Q(status=Internship.Status.PENDING)),
            accepted_by_company=Count(
                'id',
                filter=Q(status=Internship.Status.ACCEPTED_BY_COMPANY),
            ),
            validated=Count('id', filter=Q(status=Internship.Status.VALIDATED)),
            rejected=Count('id', filter=Q(status=Internship.Status.REJECTED)),
            total=Count('id'),
        )

        return Response({
            'university': admin.university.name if (admin and admin.university) else None,
            'students': {
                'total': total_students,
                'placed': placed_students,
                'unplaced': unplaced_students,
                'placement_rate': placement_rate,
            },
            'internships': status_counts,
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['Administration - Statistics'])
class StatisticsCompaniesView(APIView):
    """Company-level internship outcomes for admin's university."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        rows = _get_university_internships(request).values(
            'company_id', 'company__name',
        ).annotate(
            total_internships=Count('id'),
            pending=Count('id', filter=Q(status=Internship.Status.PENDING)),
            accepted_by_company=Count(
                'id', filter=Q(status=Internship.Status.ACCEPTED_BY_COMPANY),
            ),
            validated=Count('id', filter=Q(status=Internship.Status.VALIDATED)),
            rejected=Count('id', filter=Q(status=Internship.Status.REJECTED)),
        ).order_by('-validated', '-accepted_by_company', 'company__name')

        data = [
            {
                'company_id': row['company_id'],
                'company_name': row['company__name'],
                'total_internships': row['total_internships'],
                'pending': row['pending'],
                'accepted_by_company': row['accepted_by_company'],
                'validated': row['validated'],
                'rejected': row['rejected'],
            }
            for row in rows
        ]

        return Response({'companies': data}, status=status.HTTP_200_OK)


@extend_schema(tags=['Administration - Statistics'])
class StatisticsWilayasView(APIView):
    """Geographic distribution grouped by student or company wilaya."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        source = request.query_params.get('source', 'student')
        internships_qs = _get_university_internships(request)

        if source == 'company':
            wilaya_field = 'company__wilaya'
        else:
            source = 'student'
            wilaya_field = 'student__wilaya'

        rows = internships_qs.values(wilaya_field).annotate(
            internships_count=Count('id'),
        ).order_by('-internships_count', wilaya_field)

        data = [
            {
                'wilaya': row[wilaya_field] or 'Unknown',
                'internships_count': row['internships_count'],
            }
            for row in rows
        ]

        return Response(
            {'source': source, 'distribution': data},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=['Administration - Statistics'])
class StatisticsTrendsView(APIView):
    """Monthly or weekly internship trend aggregation."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        period = request.query_params.get('period', 'monthly')
        internships_qs = _get_university_internships(request)

        if period == 'weekly':
            bucket_expr = TruncWeek('updated_at')
            period = 'weekly'
        else:
            bucket_expr = TruncMonth('updated_at')
            period = 'monthly'

        rows = internships_qs.annotate(
            bucket=bucket_expr,
        ).values('bucket').annotate(
            placements=Count(
                'id',
                filter=Q(
                    status__in=[
                        Internship.Status.ACCEPTED_BY_COMPANY,
                        Internship.Status.VALIDATED,
                    ],
                ),
            ),
            validations=Count(
                'id', filter=Q(status=Internship.Status.VALIDATED),
            ),
            total_updates=Count('id'),
        ).order_by('bucket')

        trends = [
            {
                'period_start': row['bucket'].date().isoformat() if row['bucket'] else None,
                'placements': row['placements'],
                'validations': row['validations'],
                'total_updates': row['total_updates'],
            }
            for row in rows
        ]

        return Response(
            {'period': period, 'trends': trends},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=['Administration - Statistics'])
class StatisticsAgreementsView(APIView):
    """Agreement generation coverage for university internships."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        internships_qs = _get_university_internships(request)
        totals = internships_qs.aggregate(
            total_internships=Count('id'),
            agreements_generated=Count('id', filter=Q(agreement__isnull=False)),
        )

        total = totals['total_internships']
        generated = totals['agreements_generated']
        missing = total - generated

        return Response(
            {
                'total_internships': total,
                'agreements_generated': generated,
                'agreements_missing': missing,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=['Administration - Statistics'])
class StatisticsStatusesView(APIView):
    """Focused internship status analytics for the university."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        statuses = _get_university_internships(request).aggregate(
            pending=Count('id', filter=Q(status=Internship.Status.PENDING)),
            accepted_by_company=Count(
                'id', filter=Q(status=Internship.Status.ACCEPTED_BY_COMPANY),
            ),
            validated=Count('id', filter=Q(status=Internship.Status.VALIDATED)),
            rejected=Count('id', filter=Q(status=Internship.Status.REJECTED)),
            total=Count('id'),
        )
        return Response(statuses, status=status.HTTP_200_OK)


@extend_schema(tags=['Administration - Statistics'])
class StatisticsTrendsView(APIView):
    """Application trends over time for the university."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        period = request.query_params.get('period', 'monthly')
        qs = _get_university_internships(request)
        
        if period == 'weekly':
            trunc_func = TruncWeek('created_at')
        else:
            # Default to monthly
            trunc_func = TruncMonth('created_at')

        trends = qs.annotate(
            period_date=trunc_func
        ).values('period_date').annotate(
            count=Count('id')
        ).order_by('period_date')

        # Format output
        formatted_trends = []
        for t in trends:
            if t['period_date']:
                if period == 'weekly':
                    label = t['period_date'].strftime('%Y-W%W')
                else:
                    label = t['period_date'].strftime('%b %Y')
                formatted_trends.append({
                    'period': label,
                    'count': t['count']
                })

        return Response(formatted_trends, status=status.HTTP_200_OK)


@extend_schema(tags=['Administration - Statistics'])
class StatisticsStudentsView(APIView):
    """Student participation metrics for the admin's university."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        admin = _get_admin(request)
        from core.models import Student
        students_qs = admin.university.students.all() if admin and admin.university else Student.objects.all()

        total_students = students_qs.count()
        students_with_internships = students_qs.filter(
            internships__isnull=False,
        ).distinct().count()

        return Response(
            {
                'total_students': total_students,
                'students_with_internships': students_with_internships,
                'students_without_internships': (
                    total_students - students_with_internships
                ),
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=['Administration - Statistics'])
class StatisticsCompanyDetailView(APIView):
    """Detailed analytics for one company within admin's university scope."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, company_id):
        internships_qs = _get_university_internships(request)
        company_qs = internships_qs.filter(company_id=company_id)

        if not company_qs.exists():
            return Response(
                {'detail': 'Company not found for this university scope.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        company_name = company_qs.values_list(
            'company__name', flat=True,
        ).first()
        stats = company_qs.aggregate(
            total_internships=Count('id'),
            pending=Count('id', filter=Q(status=Internship.Status.PENDING)),
            accepted_by_company=Count(
                'id', filter=Q(status=Internship.Status.ACCEPTED_BY_COMPANY),
            ),
            validated=Count('id', filter=Q(status=Internship.Status.VALIDATED)),
            rejected=Count('id', filter=Q(status=Internship.Status.REJECTED)),
        )

        university_placements = internships_qs.filter(
            status__in=[
                Internship.Status.ACCEPTED_BY_COMPANY,
                Internship.Status.VALIDATED,
            ],
        ).count()
        company_placements = company_qs.filter(
            status__in=[
                Internship.Status.ACCEPTED_BY_COMPANY,
                Internship.Status.VALIDATED,
            ],
        ).count()
        share = round(
            (company_placements / university_placements) * 100, 2,
        ) if university_placements else 0.0

        stats.update({
            'company_id': company_id,
            'company_name': company_name,
            'company_placements': company_placements,
            'university_placements': university_placements,
            'placement_share_percent': share,
        })

        return Response(stats, status=status.HTTP_200_OK)


@extend_schema(tags=['Administration - Statistics'])
class StatisticsAtRiskView(APIView):
    """Pending internships near deadline to help early intervention."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        days = request.query_params.get('days', '14')
        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 14

        today = timezone.now().date()
        threshold = today + timedelta(days=days)

        at_risk_qs = _get_university_internships(request).filter(
            status=Internship.Status.PENDING,
            end_date__gte=today,
            end_date__lte=threshold,
        ).select_related('student', 'company').order_by('end_date')

        data = [
            {
                'internship_id': internship.id,
                'student_name': internship.student.full_name,
                'company_name': internship.company.name,
                'subject': internship.subject,
                'end_date': internship.end_date.isoformat(),
                'days_until_deadline': (internship.end_date - today).days,
            }
            for internship in at_risk_qs
        ]

        return Response(
            {
                'window_days': days,
                'count': len(data),
                'internships': data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=['Company - Statistics'])
class CompanyOfferStatsView(APIView):
    """Statistics for a specific offer belonging to the company."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]

    def get(self, request, pk):
        try:
            offer = InternshipOffer.objects.get(
                pk=pk, company__pk=request.user.pk,
            )
        except InternshipOffer.DoesNotExist:
            return Response(
                {'detail': 'Offer not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        stats = offer.applications.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status=Internship.Status.PENDING)),
            accepted=Count(
                'id', filter=Q(status=Internship.Status.ACCEPTED_BY_COMPANY),
            ),
            rejected=Count('id', filter=Q(status=Internship.Status.REJECTED)),
            validated=Count('id', filter=Q(status=Internship.Status.VALIDATED)),
        )

        data = {
            'offer_id': offer.id,
            'offer_title': offer.title,
            **stats,
        }
        return Response(data, status=status.HTTP_200_OK)


@extend_schema(tags=['Company - Statistics'])
class CompanyDashboardStatsView(APIView):
    """Aggregated stats across all offers for the authenticated company."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]

    def get(self, request):
        company_id = request.user.pk
        offers = InternshipOffer.objects.filter(company_id=company_id)

        # Overall counts
        overall = Internship.objects.filter(company_id=company_id).aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status=Internship.Status.PENDING)),
            accepted=Count(
                'id', filter=Q(status=Internship.Status.ACCEPTED_BY_COMPANY),
            ),
            rejected=Count('id', filter=Q(status=Internship.Status.REJECTED)),
            validated=Count('id', filter=Q(status=Internship.Status.VALIDATED)),
        )

        # Per-offer breakdown
        offer_breakdown = []
        for offer in offers:
            stats = offer.applications.aggregate(
                total=Count('id'),
                pending=Count('id', filter=Q(status=Internship.Status.PENDING)),
                accepted=Count(
                    'id', filter=Q(status=Internship.Status.ACCEPTED_BY_COMPANY),
                ),
                rejected=Count('id', filter=Q(status=Internship.Status.REJECTED)),
                validated=Count('id', filter=Q(status=Internship.Status.VALIDATED)),
            )
            offer_breakdown.append({
                'offer_id': offer.id,
                'offer_title': offer.title,
                **stats,
            })

        return Response({
            'overall': overall,
            'offers': offer_breakdown,
        }, status=status.HTTP_200_OK)


# ── Student Views ───────────────────────────────────────────────────

@extend_schema(tags=['Student - Notifications'])
class StudentNotificationListView(generics.ListAPIView):
    """List all notifications for the authenticated student."""
    serializer_class = StudentNotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudentUser]

    def get_queryset(self):
        return StudentNotification.objects.filter(
            recipient__pk=self.request.user.pk,
        ).select_related(
            'internship', 'internship__company', 'internship__offer',
        )


@extend_schema(tags=['Student - Notifications'])
class StudentMarkNotificationReadView(APIView):
    """Mark a student notification as read."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudentUser]

    def patch(self, request, pk):
        try:
            notification = StudentNotification.objects.get(
                pk=pk, recipient__pk=request.user.pk,
            )
        except StudentNotification.DoesNotExist:
            return Response(
                {'detail': 'Notification not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        notification.is_read = True
        notification.save()
        serializer = StudentNotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Student - Agreements'])
class StudentDownloadAgreementView(APIView):
    """Download the agreement PDF for a validated internship."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudentUser]

    def get(self, request, pk):
        try:
            # pk is internship ID
            internship = Internship.objects.select_related(
                'agreement',
            ).get(pk=pk, student__pk=request.user.pk)
        except Internship.DoesNotExist:
            return Response(
                {'detail': 'Internship not found.'},
                status=status.HTTP_404_NOT_FOUND,
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


@extend_schema(tags=['Student - Internships'])
class StudentInternshipListCreateView(generics.ListCreateAPIView):
    """List my internship applications or create a new one."""
    serializer_class = InternshipApplySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudentUser]

    def get_queryset(self):
        return Internship.objects.filter(
            student__pk=self.request.user.pk,
        ).select_related('offer', 'company')

    def create(self, request, *args, **kwargs):
        """Prevent duplicate applications to the same offer."""
        offer_id = request.data.get('offer_id')
        if offer_id:
            already = Internship.objects.filter(
                student__pk=request.user.pk,
                offer_id=offer_id,
            ).exists()
            if already:
                return Response(
                    {'detail': 'You have already applied to this offer.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        internship = serializer.save()
        # Create notification for the company
        try:
            company_obj = Company.objects.get(pk=internship.company_id)
            offer_title = internship.offer.title if (internship.offer and internship.offer.title) else internship.subject
            CompanyNotification.objects.create(
                recipient=company_obj,
                internship=internship,
                notification_type=CompanyNotification.Type.NEW_APPLICATION,
                message=f'New application from {internship.student.full_name} for: {offer_title}.',
            )
            
            # Also notify Admins
            university = internship.student.university
            admin_users = User.objects.filter(role=User.Roles.ADMIN, is_active=True)
            to_notify = []
            for u in admin_users:
                try:
                    admin_profile = u.admin
                    if university:
                        if admin_profile.university == university or admin_profile.university is None:
                            to_notify.append(u)
                    else:
                        if admin_profile.university is None:
                            to_notify.append(u)
                except Exception:
                    to_notify.append(u)

            for recipient in to_notify:
                Notification.objects.create(
                    recipient=recipient,
                    internship=internship,
                    notification_type=Notification.Type.NEW_APPLICATION,
                    message=f'New internship application from {internship.student.full_name} to {company_obj.name}.',
                )
        except Exception as e:
            import traceback
            print(f"[NOTIFICATION ERROR] {e}\n{traceback.format_exc()}")

# ── Company Views ───────────────────────────────────────────────────

@extend_schema(tags=['Company - Internships'])
class CompanyInternshipListView(generics.ListAPIView):
    """List all internship requests for the authenticated company."""
    serializer_class = CompanyInternshipSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]

    def get_queryset(self):
        return Internship.objects.filter(company_id=self.request.user.id)


@extend_schema(tags=['Company - Internships'])
class CompanyAcceptInternshipView(APIView):
    """Accept an internship request as a company."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]

    def patch(self, request, pk):
        try:
            internship = Internship.objects.get(
                pk=pk, company__pk=request.user.pk,
            )
        except Internship.DoesNotExist:
            return Response(
                {'detail': 'Internship not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if internship.status != Internship.Status.PENDING:
            return Response(
                {'detail': 'Only pending internships can be accepted.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        internship.status = Internship.Status.ACCEPTED_BY_COMPANY
        internship.save()

        # Create notification for admins
        university = internship.student.university
        
        # Get all users with role 'admin'
        # We also want to include superusers (who might not have an Admin profile record)
        admin_users = User.objects.filter(role=User.Roles.ADMIN, is_active=True)
        
        # If the student belongs to a university, we filter admins by that university
        # or we notify all global admins (no university)
        to_notify = []
        for u in admin_users:
            try:
                admin_profile = u.admin
                if university:
                    if admin_profile.university == university or admin_profile.university is None:
                        to_notify.append(u)
                else:
                    if admin_profile.university is None:
                        to_notify.append(u)
            except Exception:
                to_notify.append(u)

        print(f"[DEBUG] Notifying {len(to_notify)} admins for internship {internship.id}")
        for recipient in to_notify:
            Notification.objects.create(
                recipient=recipient,
                internship=internship,
                notification_type=Notification.Type.INTERNSHIP_ACCEPTED,
                message=f'New internship request from {internship.student.full_name} accepted by {internship.company.name}.',
            )
            print(f"[DEBUG] Created notification for {recipient.email}")

        return Response(CompanyInternshipSerializer(internship).data)


@extend_schema(tags=['Company - Internships'])
class CompanyRejectInternshipView(APIView):
    """Reject an internship request as a company."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]

    def patch(self, request, pk):
        try:
            internship = Internship.objects.get(
                pk=pk, company__pk=request.user.pk,
            )
        except Internship.DoesNotExist:
            return Response(
                {'detail': 'Internship not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        internship.status = Internship.Status.REJECTED
        internship.save()

        # Notify the student that their application was rejected by the company
        StudentNotification.objects.create(
            recipient=internship.student,
            internship=internship,
            notification_type=StudentNotification.Type.INTERNSHIP_REJECTED,
            message=f'Unfortunately, your application for "{internship.offer.title if internship.offer else internship.subject}" was rejected by {internship.company.name}.',
        )

        return Response(CompanyInternshipSerializer(internship).data)


# ── Public Views ────────────────────────────────────────────────────

@extend_schema(tags=['Public'])
class PublicInternshipOfferListView(generics.ListAPIView):
    """List all active internship offers (for students/landing page)."""
    serializer_class = InternshipOfferSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = InternshipOffer.objects.filter(is_active=True)
        search = self.request.query_params.get('search', None)
        offer_type = self.request.query_params.get('type', None)
        
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(title__icontains=search) | 
                Q(company__name__icontains=search) | 
                Q(location__icontains=search)
            )
        
        if offer_type and offer_type in ['paid', 'unpaid']:
            qs = qs.filter(type=offer_type)
            
        return qs


@extend_schema(tags=['Public'])
class PublicInternshipOfferDetailView(generics.RetrieveAPIView):
    """Retrieve details of a specific active internship offer."""
    queryset = InternshipOffer.objects.filter(is_active=True)
    serializer_class = InternshipOfferSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=['Public'])
class PublicCompanyListView(generics.ListAPIView):
    """List all companies (for landing page)."""
    queryset = Company.objects.all()
    serializer_class = CompanyPublicSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=['Company - Offers'])
class CompanyInternshipOfferListCreateView(generics.ListCreateAPIView):
    """List or create internship offers for the authenticated company."""
    serializer_class = InternshipOfferSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]

    def get_queryset(self):
        return InternshipOffer.objects.filter(company__pk=self.request.user.pk)

    def perform_create(self, serializer):
        company = Company.objects.get(pk=self.request.user.pk)
        serializer.save(company=company)


@extend_schema(tags=['Company - Offers'])
class CompanyInternshipOfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Manage a single internship offer."""
    serializer_class = InternshipOfferSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]

    def get_queryset(self):
        return InternshipOffer.objects.filter(company__pk=self.request.user.pk)


@extend_schema(tags=['Company - Offers'])
class CompanyOfferImageUploadView(generics.UpdateAPIView):
    """Upload an image for a specific internship offer."""
    serializer_class = InternshipOfferSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['patch']

    def get_queryset(self):
        return InternshipOffer.objects.filter(company__pk=self.request.user.pk)


@extend_schema(tags=['Company - Offers'])
class CompanyOfferApplicantsView(generics.ListAPIView):
    """List all applications for a specific offer."""
    serializer_class = CompanyInternshipSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]

    def get_queryset(self):
        return Internship.objects.filter(
            offer_id=self.kwargs['pk'],
            company__pk=self.request.user.pk
        ).select_related('student')


# ── Data Reset Views ──────────────────────────────────────────────────

@extend_schema(tags=['Administration - Reset'])
class AdminResetDataView(APIView):
    """
    Reset all dashboard data across the platform.
    Requires Admin password confirmation.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        password = request.data.get('password')
        if not password or not request.user.check_password(password):
            return Response(
                {'detail': 'Invalid password.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Wipe all platform data
        Internship.objects.all().delete()
        InternshipOffer.objects.all().delete()
        Notification.objects.all().delete()
        StudentNotification.objects.all().delete()
        
        return Response({'detail': 'All platform data has been reset successfully.'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Company - Reset'])
class CompanyResetDataView(APIView):
    """
    Reset dashboard data for the authenticated company.
    Requires Company password confirmation.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]

    def post(self, request):
        password = request.data.get('password')
        if not password or not request.user.check_password(password):
            return Response(
                {'detail': 'Invalid password.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        company_id = request.user.pk
        
        # Wipe company-specific data
        Internship.objects.filter(company_id=company_id).delete()
        InternshipOffer.objects.filter(company_id=company_id).delete()
        
        return Response({'detail': 'Company dashboard data has been reset successfully.'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Company - Notifications'])
class CompanyNotificationListView(generics.ListAPIView):
    """List all notifications for the authenticated company."""
    serializer_class = CompanyNotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]

    def get_queryset(self):
        return CompanyNotification.objects.filter(
            recipient_id=self.request.user.id
        ).order_by('-created_at')


@extend_schema(tags=['Company - Notifications'])
class MarkCompanyNotificationsReadView(APIView):
    """Mark all notifications for the authenticated company as read."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyUser]

    def patch(self, request):
        CompanyNotification.objects.filter(
            recipient__pk=request.user.pk,
            is_read=False,
        ).update(is_read=True)
        return Response(status=status.HTTP_200_OK)
