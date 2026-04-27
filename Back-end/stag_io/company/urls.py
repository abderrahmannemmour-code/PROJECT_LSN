"""URL mappings for the company app."""
from django.urls import path
from company import views

app_name = 'company'

urlpatterns = [
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
]