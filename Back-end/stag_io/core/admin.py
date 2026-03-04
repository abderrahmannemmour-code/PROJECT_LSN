"""Django admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
    """Admin page for base User model."""
    ordering = ['id']
    list_display = ['email', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Role'), {'fields': ('role',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


class StudentAdmin(BaseUserAdmin):
    """Admin page for Students."""
    ordering = ['id']
    list_display = ['email', 'full_name', 'wilaya', 'is_active']
    search_fields = ['email', 'full_name']
    list_filter = ['wilaya', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Student Info'), {'fields': ('full_name', 'university', 'wilaya', 'github_link', 'portfolio_link', 'profile_image')}),
        (_('Permissions'), {'fields': ('is_active',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'full_name', 'university', 'wilaya'),
        }),
    )


class CompanyAdmin(BaseUserAdmin):
    """Admin page for Companies."""
    ordering = ['id']
    list_display = ['email', 'name', 'wilaya', 'is_active']
    search_fields = ['email', 'name']
    list_filter = ['wilaya', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Company Info'), {'fields': ('name', 'description', 'logo', 'wilaya', 'website')}),
        (_('Permissions'), {'fields': ('is_active',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'wilaya'),
        }),
    )


class AdminProfileAdmin(BaseUserAdmin):
    """Admin page for Admins."""
    ordering = ['id']
    list_display = ['email', 'title', 'department', 'is_active']
    search_fields = ['email', 'title']
    list_filter = ['department', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Admin Info'), {'fields': ('university', 'department', 'title')}),
        (_('Permissions'), {'fields': ('is_active',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'university', 'department', 'title'),
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.Admin, AdminProfileAdmin)
admin.site.register(models.University)
admin.site.register(models.Internship)
admin.site.register(models.Notification)