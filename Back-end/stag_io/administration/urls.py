"""URL mappings for the administration API."""
from django.urls import path

from administration import views

app_name = 'administration'

urlpatterns = [
    path(
        'internships/',
        views.AllInternshipListView.as_view(),
        name='internship-list',
    ),
    path(
        'internships/pending/',
        views.PendingInternshipListView.as_view(),
        name='internship-pending',
    ),
    path(
        'internships/<int:pk>/',
        views.InternshipDetailView.as_view(),
        name='internship-detail',
    ),
    path(
        'internships/<int:pk>/validate/',
        views.ValidateInternshipView.as_view(),
        name='internship-validate',
    ),
    path(
        'internships/<int:pk>/reject/',
        views.RejectInternshipView.as_view(),
        name='internship-reject',
    ),
]
