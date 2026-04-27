"""Views for the company internship offer API."""
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Company, InternshipOffer
from company.serializers import (
    InternshipOfferSerializer,
    CreateInternshipOfferSerializer,
    UpdateInternshipOfferSerializer,
)
from user.views import IsCompany


def get_company(request):
    """Get the Company object for the currently logged-in user."""
    return Company.objects.get(pk=request.user.pk)


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
        """Returns all offers posted by the logged-in company."""
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
        """Creates a new internship offer for the logged-in company."""
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
        """Fetch offer by ID and verify it belongs to this company."""
        try:
            return InternshipOffer.objects.get(pk=pk, company=company)
        except InternshipOffer.DoesNotExist:
            return None

    @extend_schema(responses={200: InternshipOfferSerializer})
    def get(self, request, pk):
        """View details of one specific offer."""
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
        """
        Partially update an offer.
        Only send the fields you want to change.
        """
        company = get_company(request)
        offer = self.get_offer(pk, company)
        if not offer:
            return Response(
                {'detail': 'Offer not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UpdateInternshipOfferSerializer(
            offer,
            data=request.data,
            partial=True,
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
        """
        Delete an offer permanently.
        The frontend handles the confirmation dialog.
        Returns 204 No Content on success.
        """
        company = get_company(request)
        offer = self.get_offer(pk, company)
        if not offer:
            return Response(
                {'detail': 'Offer not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)