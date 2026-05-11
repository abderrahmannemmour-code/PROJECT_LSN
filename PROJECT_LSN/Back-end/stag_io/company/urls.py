"""URL mappings for the company app."""
from django.urls import path
from company import views

app_name = 'company'

urlpatterns = [
    # Offer management
    path(
        'offers/',
        views.OfferListCreateView.as_view(),
        name='offer-list-create',
    ),
    path(
        'offers/<int:pk>/',
        views.OfferDetailView.as_view(),
        name='offer-detail',
    ),
    # Applicant management
    path(
        'offers/<int:pk>/applicants/',
        views.OfferApplicantListView.as_view(),
        name='offer-applicants',
    ),
    path(
        'applications/',
        views.AllApplicantsListView.as_view(),
        name='all-applications',
    ),
    path(
        'applications/<int:pk>/accept/',
        views.AcceptApplicantView.as_view(),
        name='application-accept',
    ),
    path(
        'applications/<int:pk>/reject/',
        views.RejectApplicantView.as_view(),
        name='application-reject',
    ),
]