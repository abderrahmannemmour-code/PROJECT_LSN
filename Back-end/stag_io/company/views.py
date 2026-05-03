"""Views for the company internship offer and applicant management API."""
from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Company, InternshipOffer, Internship, Notification, Admin
from company.serializers import (
    InternshipOfferSerializer,
    CreateInternshipOfferSerializer,
    UpdateInternshipOfferSerializer,
    ApplicantSerializer,
)
from user.views import IsCompany


def get_company(request):
    """Get the Company object for the currently logged-in user."""
    return Company.objects.get(pk=request.user.pk)


# ── Offer views ──────────────────────────────────────────────────────

@extend_schema(tags=['Company Offers'])
class OfferListCreateView(APIView):
    """
    GET  /api/company/offers/ — list this company's offers
    POST /api/company/offers/ — create a new offer
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @extend_schema(responses={200: InternshipOfferSerializer(many=True)})
    def get(self, request):
        company = get_company(request)
        offers = InternshipOffer.objects.filter(company=company)
        serializer = InternshipOfferSerializer(
            offers, many=True, context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CreateInternshipOfferSerializer,
        responses={201: InternshipOfferSerializer},
    )
    def post(self, request):
        serializer = CreateInternshipOfferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        company = get_company(request)
        offer = serializer.save(company=company)
        return Response(
            InternshipOfferSerializer(
                offer, context={'request': request},
            ).data,
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=['Company Offers'])
class OfferDetailView(APIView):
    """
    GET    /api/company/offers/<id>/ — view a specific offer
    PATCH  /api/company/offers/<id>/ — modify an offer
    DELETE /api/company/offers/<id>/ — delete an offer
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_offer(self, pk, company):
        try:
            return InternshipOffer.objects.get(pk=pk, company=company)
        except InternshipOffer.DoesNotExist:
            return None

    @extend_schema(responses={200: InternshipOfferSerializer})
    def get(self, request, pk):
        company = get_company(request)
        offer = self.get_offer(pk, company)
        if not offer:
            return Response(
                {'detail': 'Offer not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = InternshipOfferSerializer(
            offer, context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=UpdateInternshipOfferSerializer,
        responses={200: InternshipOfferSerializer},
    )
    def patch(self, request, pk):
        company = get_company(request)
        offer = self.get_offer(pk, company)
        if not offer:
            return Response(
                {'detail': 'Offer not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UpdateInternshipOfferSerializer(
            offer, data=request.data, partial=True,
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        offer = serializer.save()
        return Response(
            InternshipOfferSerializer(
                offer, context={'request': request},
            ).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(responses={204: None})
    def delete(self, request, pk):
        company = get_company(request)
        offer = self.get_offer(pk, company)
        if not offer:
            return Response(
                {'detail': 'Offer not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Applicant management views ───────────────────────────────────────

@extend_schema(tags=['Company Applicants'])
class OfferApplicantListView(generics.ListAPIView):
    """
    GET /api/company/offers/<id>/applicants/
    List all students who applied to one of this company's offers.
    Shows applicant profile info and their current application status.
    """
    serializer_class = ApplicantSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]

    def get_queryset(self):
        company = get_company(self.request)
        offer_id = self.kwargs['pk']

        # Make sure the offer belongs to this company
        try:
            offer = InternshipOffer.objects.get(pk=offer_id, company=company)
        except InternshipOffer.DoesNotExist:
            return Internship.objects.none()

        return Internship.objects.filter(
            offer=offer,
        ).select_related(
            'student', 'offer',
        ).prefetch_related(
            'student__student_skills__skill',
        ).order_by('-created_at')


@extend_schema(tags=['Company Applicants'])
class AcceptApplicantView(APIView):
    """
    POST /api/company/applications/<id>/accept/
    Company accepts a student's application.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]

    def post(self, request, pk):
        company = get_company(request)

        # 1. Get the application and verify it belongs to this company
        try:
            application = Internship.objects.select_related(
                'student', 'student__university', 'company', 'offer',
            ).get(pk=pk, company=company)
        except Internship.DoesNotExist:
            return Response(
                {'detail': 'Application not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 2. Can only accept pending applications
        if application.status != Internship.Status.PENDING:
            return Response(
                {
                    'detail': (
                        f'Cannot accept this application. '
                        f'Current status is: {application.status}'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3. Update status
        application.status = Internship.Status.ACCEPTED_BY_COMPANY
        application.save()

        # 5. Send notification to all admins of the student's university
        #    so they can validate or reject the internship
        self._notify_admins(application)

        return Response(
            {
                'detail': 'Application accepted successfully. '
                          'The university has been notified.',
                'application_id': application.id,
                'status': application.status,
            },
            status=status.HTTP_200_OK,
        )

    def _notify_admins(self, application):
        """
        Create a Notification for every admin in the student's university.
        If the student has no university set, no notification is sent
        (edge case — shouldn't happen in production).
        """
        university = application.student.university
        if not university:
            return

        admins = Admin.objects.filter(university=university)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                internship=application,
                notification_type=Notification.Type.INTERNSHIP_ACCEPTED,
                message=(
                    f'{application.student.full_name} has been accepted by '
                    f'{application.company.name} for the internship: '
                    f'"{application.subject}". '
                    f'Please review and validate or reject this internship.'
                ),
            )


@extend_schema(tags=['Company Applicants'])
class RejectApplicantView(APIView):
    """
    POST /api/company/applications/<id>/reject/
    Company rejects a student's application.

    Only pending applications can be rejected.
    The offer stays open so other students can still apply.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]

    def post(self, request, pk):
        company = get_company(request)

        try:
            application = Internship.objects.select_related(
                'student', 'company', 'offer',
            ).get(pk=pk, company=company)
        except Internship.DoesNotExist:
            return Response(
                {'detail': 'Application not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if application.status != Internship.Status.PENDING:
            return Response(
                {
                    'detail': (
                        f'Cannot reject this application. '
                        f'Current status is: {application.status}'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = Internship.Status.REJECTED
        application.save()

        return Response(
            {
                'detail': 'Application rejected.',
                'application_id': application.id,
                'status': application.status,
            },
            status=status.HTTP_200_OK,
        )