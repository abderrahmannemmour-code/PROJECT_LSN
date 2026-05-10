"""Permissions for the administration API."""
from rest_framework import permissions

from core.models import Admin


class IsAdminUser(permissions.BasePermission):
    """Allow access only to users with admin role."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsAdminOfSameUniversity(permissions.BasePermission):
    """Admin can only access internships for students of their university."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.role != 'admin':
            return False
        # If user is superuser or has no Admin record, we consider them global admins
        try:
            Admin.objects.get(pk=request.user.pk)
        except Admin.DoesNotExist:
            return True
        return True

    def has_object_permission(self, request, view, obj):
        try:
            admin = Admin.objects.get(pk=request.user.pk)
        except Admin.DoesNotExist:
            # Superusers/Global admins can access everything
            return True

        # If admin has no university assigned, they are global
        if not admin.university:
            return True

        # obj is an Internship — check student's university
        if hasattr(obj, 'student') and hasattr(obj.student, 'university'):
            # If student has no university, only global admins (or same university admins, which is None=None)
            return obj.student.university == admin.university

        return True


class IsStudentUser(permissions.BasePermission):
    """Allow access only to users with student role."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'student'
        )


class IsCompanyUser(permissions.BasePermission):
    """Allow access only to users with company role."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'company'
        )
