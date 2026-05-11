"""Views for the company internship offer and applicant management API."""
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Company, InternshipOffer, Internship
from core.notifications import (
    notify_admins_internship_accepted,
    notify_student_accepted,
    notify_student_rejected,
)
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
    """
    serializer_class = ApplicantSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]

    def get_queryset(self):
        company = get_company(self.request)
        offer_id = self.kwargs['pk']
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
class AllApplicantsListView(generics.ListAPIView):
    """
    GET /api/company/applications/
    List all students who applied to any of this company's offers.
    """
    serializer_class = ApplicantSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]

    def get_queryset(self):
        company = get_company(self.request)
        return Internship.objects.filter(
            company=company,
        ).select_related(
            'student', 'offer',
        ).prefetch_related(
            'student__student_skills__skill',
        ).order_by('-created_at')


@extend_schema(tags=['Company Applicants'])
class AcceptApplicantView(APIView):
    """
    POST /api/company/applications/<id>/accept/
    Company accepts a student. Notifies student and all university admins.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]

    @extend_schema(request=None, responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT})
    def post(self, request, pk):
        company = get_company(request)
        try:
            application = Internship.objects.select_related(
                'student', 'student__university', 'company', 'offer',
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
                        f'Cannot accept this application. '
                        f'Current status is: {application.status}'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = Internship.Status.ACCEPTED_BY_COMPANY
        application.save()

        # Notify student they were accepted
        notify_student_accepted(application)
        # Notify all admins of the student's university
        notify_admins_internship_accepted(application)

        return Response(
            {
                'detail': 'Application accepted. Student and university notified.',
                'application_id': application.id,
                'status': application.status,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=['Company Applicants'])
class RejectApplicantView(APIView):
    """
    POST /api/company/applications/<id>/reject/
    Company rejects a student's application. Notifies the student.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompany]

    @extend_schema(request=None, responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT})
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

        # Notify student they were rejected
        notify_student_rejected(application)

        return Response(
            {
                'detail': 'Application rejected. Student has been notified.',
                'application_id': application.id,
                'status': application.status,
            },
            status=status.HTTP_200_OK,
        )