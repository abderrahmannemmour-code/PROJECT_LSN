"""stag_io URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from administration import views as admin_views
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),

    # ── 1. AUTH & USER ──
    path('api/user/', include('user.urls')),

    # ── 2. SHARED NOTIFICATIONS ──
    path('api/notifications/', include([
        path('', admin_views.NotificationListView.as_view(), name='notif-list'),
        path('unread/', admin_views.UnreadNotificationListView.as_view(), name='notif-unread'),
        path('read-all/', admin_views.MarkAllNotificationsReadView.as_view(), name='notif-read-all'),
        path('<int:pk>/read/', admin_views.MarkNotificationReadView.as_view(), name='notif-read'),
    ])),

    # ── 3. STUDENT ENDPOINTS ──
    path('api/student/', include([
        path('skills/', user_views.SkillListView.as_view(), name='student-skills-list'),
        path('me/skills/', user_views.MySkillListView.as_view(), name='student-skills-me'),
        path('me/skills/add/', user_views.AddSkillView.as_view(), name='student-skills-add'),
        path('me/skills/<int:pk>/remove/', user_views.RemoveSkillView.as_view(), name='student-skills-remove'),
        path('offers/', admin_views.PublicInternshipOfferListView.as_view(), name='student-offers'),
        path('offers/<int:pk>/', admin_views.PublicInternshipOfferDetailView.as_view(), name='student-offer-detail'),
        path('offers/<int:pk>/apply/', admin_views.StudentInternshipListCreateView.as_view(), name='student-apply'),
        path('applications/', admin_views.StudentInternshipListCreateView.as_view(), name='student-apps'),
        path('universities/', user_views.UniversityListView.as_view(), name='student-universities'),
        path('me/cv/', user_views.StudentUpdateView.as_view(), name='student-cv'),
    ])),

    # ── 4. COMPANY ENDPOINTS ──
    path('api/company/', include([
        path('offers/', admin_views.CompanyInternshipOfferListCreateView.as_view(), name='company-offers'),
        path('offers/<int:pk>/', admin_views.CompanyInternshipOfferDetailView.as_view(), name='company-offer-detail'),
        path('offers/<int:pk>/applicants/', admin_views.CompanyOfferApplicantsView.as_view(), name='company-offer-applicants'),
        path('offers/<int:pk>/upload-image/', admin_views.CompanyOfferImageUploadView.as_view(), name='company-offer-image-upload'),
        path('applications/', admin_views.CompanyInternshipListView.as_view(), name='company-apps'),
        path('applications/<int:pk>/accept/', admin_views.CompanyAcceptInternshipView.as_view(), name='company-accept'),
        path('applications/<int:pk>/reject/', admin_views.CompanyRejectInternshipView.as_view(), name='company-reject'),
        path('stats/', admin_views.CompanyDashboardStatsView.as_view(), name='company-dashboard-stats'),
        path('offers/<int:pk>/stats/', admin_views.CompanyOfferStatsView.as_view(), name='company-offer-stats'),
        path('reset-data/', admin_views.CompanyResetDataView.as_view(), name='company-reset'),
        path('notifications/', admin_views.CompanyNotificationListView.as_view(), name='company-notification-list'),
        path('notifications/mark-read/', admin_views.MarkCompanyNotificationsReadView.as_view(), name='company-notification-mark-read'),
    ])),

    # ── 5. ADMINISTRATION ENDPOINTS ──
    path('api/administration/', include('administration.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
