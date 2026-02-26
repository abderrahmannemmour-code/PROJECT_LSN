from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path(
        'register/student/',
        views.StudentRegisterView.as_view(),
        name='register-student',
    ),
    path(
        'register/company/',
        views.CompanyRegisterView.as_view(),
        name='register-company',
    ),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token-obtain',
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token-refresh',
    ),
    path(
        'me/',
        views.ManageUserView.as_view(),
        name='me',
    ),
    path(
        '<int:pk>/delete/',
        views.AdminDeleteUserView.as_view(),
        name='admin-delete-user',
    ),
]
