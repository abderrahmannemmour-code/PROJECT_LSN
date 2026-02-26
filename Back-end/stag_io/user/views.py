"""Views for the user API."""
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import (
    StudentRegisterSerializer,
    CompanyRegisterSerializer,
    UserDetailSerializer,
)


class IsAdmin(permissions.BasePermission):
    """Allow access only to Django staff admins (is_staff=True)."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class StudentRegisterView(generics.CreateAPIView):
    """Register a new student."""
    serializer_class = StudentRegisterSerializer


class CompanyRegisterView(generics.CreateAPIView):
    """Register a new company."""
    serializer_class = CompanyRegisterSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user (GET /me, PATCH /me)."""
    serializer_class = UserDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the authenticated user."""
        return self.request.user


class AdminDeleteUserView(generics.DestroyAPIView):
    """Allow an admin to delete any user by ID."""
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    lookup_field = 'pk'