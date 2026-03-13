"""URL mappings for the administration API."""
from django.urls import path

from administration import views

app_name = 'administration'

urlpatterns = [
    # Notifications
    path(
        'notifications/',
        views.NotificationListView.as_view(),
        name='notification-list',
    ),
    path(
        'notifications/unread/',
        views.UnreadNotificationListView.as_view(),
        name='notification-unread',
    ),
    path(
        'notifications/<int:pk>/read/',
        views.MarkNotificationReadView.as_view(),
        name='notification-read',
    ),
    # Internships
    path(
        'internships/',
        views.AllInternshipListView.as_view(),
        name='internship-list',
    ),
    path(
        'internships/<int:pk>/',
        views.InternshipDetailView.as_view(),
        name='internship-detail',
    ),
    path(
        'internships/<int:pk>/agreement/',
        views.DownloadInternshipAgreementView.as_view(),
        name='internship-agreement-download',
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
