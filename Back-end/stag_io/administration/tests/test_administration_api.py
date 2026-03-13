"""Tests for the administration API."""
from datetime import date
from unittest.mock import patch

from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    InternshipAgreement,
    University,
    Student,
    Company,
    Admin,
    Internship,
    Notification,
)


INTERNSHIP_LIST_URL = reverse('administration:internship-list')
NOTIFICATION_LIST_URL = reverse('administration:notification-list')
NOTIFICATION_UNREAD_URL = reverse('administration:notification-unread')


def internship_detail_url(internship_id):
    return reverse('administration:internship-detail', args=[internship_id])


def internship_validate_url(internship_id):
    return reverse('administration:internship-validate', args=[internship_id])


def internship_reject_url(internship_id):
    return reverse('administration:internship-reject', args=[internship_id])


def internship_agreement_download_url(internship_id):
    return reverse('administration:internship-agreement-download', args=[internship_id])


def notification_read_url(notification_id):
    return reverse('administration:notification-read', args=[notification_id])


def create_university(**params):
    defaults = {
        'name': 'University of Test',
        'code': 'UOT',
        'wilaya': 'Algiers',
    }
    defaults.update(params)
    return University.objects.create(**defaults)


def create_student(university, **params):
    defaults = {
        'email': 'student@example.com',
        'password': 'testpass123',
        'full_name': 'Test Student',
        'wilaya': 'Algiers',
    }
    defaults.update(params)
    student = Student.objects.create_user(**defaults)
    student.university = university
    student.role = 'student'
    student.save()
    return student


def create_company(**params):
    defaults = {
        'email': 'company@example.com',
        'password': 'testpass123',
        'name': 'Test Company',
        'wilaya': 'Algiers',
    }
    defaults.update(params)
    company = Company.objects.create_user(**defaults)
    company.role = 'company'
    company.save()
    return company


def create_admin_user(university, **params):
    defaults = {
        'email': 'admin@example.com',
        'password': 'testpass123',
        'department': 'CS',
        'title': 'Head of Department',
    }
    defaults.update(params)
    admin = Admin.objects.create_user(**defaults)
    admin.university = university
    admin.role = 'admin'
    admin.save()
    return admin


def create_internship(student, company, **params):
    defaults = {
        'subject': 'Django Development',
        'description': 'Building APIs',
        'start_date': date(2026, 4, 1),
        'end_date': date(2026, 6, 30),
        'status': Internship.Status.ACCEPTED_BY_COMPANY,
    }
    defaults.update(params)
    return Internship.objects.create(
        student=student, company=company, **defaults,
    )


def create_notification(recipient, internship, **params):
    defaults = {
        'notification_type': Notification.Type.INTERNSHIP_ACCEPTED,
        'message': f'{internship.company.name} accepted {internship.student.full_name}',
    }
    defaults.update(params)
    return Notification.objects.create(
        recipient=recipient, internship=internship, **defaults,
    )


def create_internship_agreement(internship, file_name='agreement.pdf'):
    agreement = InternshipAgreement.objects.create(internship=internship)
    agreement.pdf_file.save(
        file_name,
        ContentFile(b'%PDF-1.4 test agreement'),
        save=True,
    )
    return agreement


class PublicAdministrationApiTests(TestCase):
    """Test unauthenticated access is denied."""

    def setUp(self):
        self.client = APIClient()

    def test_internship_list_requires_auth(self):
        res = self.client.get(INTERNSHIP_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class NonAdminAccessTests(TestCase):
    """Test that non-admin users cannot access admin endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.university = create_university()
        self.student = create_student(self.university)
        self.client.force_authenticate(user=self.student)

    def test_student_cannot_list_internships(self):
        res = self.client.get(INTERNSHIP_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminInternshipListTests(TestCase):
    """Test admin internship list endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.university = create_university()
        self.other_university = create_university(
            name='Other University', code='OTH',
        )
        self.admin_user = create_admin_user(self.university)
        self.student = create_student(self.university)
        self.company = create_company()
        self.client.force_authenticate(user=self.admin_user)

    def test_list_all_internships_for_university(self):
        """Admin sees only internships for their university's students."""
        create_internship(self.student, self.company)

        # Student from other university
        other_student = create_student(
            self.other_university,
            email='other@example.com',
            full_name='Other Student',
        )
        create_internship(other_student, self.company)

        res = self.client.get(INTERNSHIP_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(
            res.data[0]['student_name'], self.student.full_name,
        )


class AdminValidateRejectTests(TestCase):
    """Test validate and reject endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.university = create_university()
        self.admin_user = create_admin_user(self.university)
        self.student = create_student(self.university)
        self.company = create_company()
        self.client.force_authenticate(user=self.admin_user)

    @patch('administration.views.generate_internship_agreement')
    def test_validate_internship(self, mock_generate_agreement):
        internship = create_internship(self.student, self.company)

        res = self.client.patch(internship_validate_url(internship.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        internship.refresh_from_db()
        self.assertEqual(internship.status, Internship.Status.VALIDATED)
        mock_generate_agreement.assert_called_once_with(
            internship, admin=self.admin_user,
        )

    @patch(
        'administration.views.generate_internship_agreement',
        side_effect=ValueError('No administrator found for this university.'),
    )
    def test_validate_internship_rolls_back_when_agreement_generation_fails(
        self, mock_generate_agreement,
    ):
        internship = create_internship(self.student, self.company)

        res = self.client.patch(internship_validate_url(internship.id))

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['detail'],
            'No administrator found for this university.',
        )
        internship.refresh_from_db()
        self.assertEqual(
            internship.status,
            Internship.Status.ACCEPTED_BY_COMPANY,
        )
        mock_generate_agreement.assert_called_once_with(
            internship, admin=self.admin_user,
        )

    def test_reject_internship(self):
        internship = create_internship(self.student, self.company)

        res = self.client.patch(internship_reject_url(internship.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        internship.refresh_from_db()
        self.assertEqual(internship.status, Internship.Status.REJECTED)

    def test_cannot_validate_pending_internship(self):
        """Can only validate if status is accepted_by_company."""
        internship = create_internship(
            self.student, self.company,
            status=Internship.Status.PENDING,
        )

        res = self.client.patch(internship_validate_url(internship.id))

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_reject_already_validated(self):
        internship = create_internship(
            self.student, self.company,
            status=Internship.Status.VALIDATED,
        )

        res = self.client.patch(internship_reject_url(internship.id))

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_cannot_validate_other_university_internship(self):
        """Admin from university A cannot validate university B's internship."""
        other_uni = create_university(name='Other Uni', code='OTH')
        other_student = create_student(
            other_uni,
            email='otherstudent@example.com',
            full_name='Other Student',
        )
        internship = create_internship(other_student, self.company)

        res = self.client.patch(internship_validate_url(internship.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PublicNotificationApiTests(TestCase):
    """Test unauthenticated access to notification endpoints is denied."""

    def setUp(self):
        self.client = APIClient()

    def test_notification_list_requires_auth(self):
        res = self.client.get(NOTIFICATION_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unread_notifications_requires_auth(self):
        res = self.client.get(NOTIFICATION_UNREAD_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class NonAdminNotificationAccessTests(TestCase):
    """Test that non-admin users cannot access notification endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.university = create_university()
        self.student = create_student(self.university)
        self.client.force_authenticate(user=self.student)

    def test_student_cannot_list_notifications(self):
        res = self.client.get(NOTIFICATION_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_list_unread_notifications(self):
        res = self.client.get(NOTIFICATION_UNREAD_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminNotificationTests(TestCase):
    """Test admin notification endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.university = create_university()
        self.admin_user = create_admin_user(self.university)
        self.student = create_student(self.university)
        self.company = create_company()
        self.client.force_authenticate(user=self.admin_user)

    def test_list_notifications(self):
        """Admin sees their own notifications."""
        internship = create_internship(self.student, self.company)
        create_notification(self.admin_user, internship)

        res = self.client.get(NOTIFICATION_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['student_name'], self.student.full_name)
        self.assertEqual(res.data[0]['company_name'], self.company.name)

    def test_list_unread_notifications(self):
        """Only unread notifications are returned."""
        internship = create_internship(self.student, self.company)
        create_notification(self.admin_user, internship)
        create_notification(
            self.admin_user, internship, is_read=True,
        )

        res = self.client.get(NOTIFICATION_UNREAD_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertFalse(res.data[0]['is_read'])

    def test_mark_notification_as_read(self):
        """PATCH marks a notification as read."""
        internship = create_internship(self.student, self.company)
        notification = create_notification(self.admin_user, internship)

        res = self.client.patch(notification_read_url(notification.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_cannot_read_other_admin_notification(self):
        """Admin cannot mark another admin's notification as read."""
        other_uni = create_university(name='Other Uni', code='OTH')
        other_admin = create_admin_user(
            other_uni, email='other_admin@example.com',
        )
        internship = create_internship(self.student, self.company)
        notification = create_notification(other_admin, internship)

        res = self.client.patch(notification_read_url(notification.id))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_only_sees_own_notifications(self):
        """Admin does not see notifications for other admins."""
        other_uni = create_university(name='Other Uni', code='OTH')
        other_admin = create_admin_user(
            other_uni, email='other_admin@example.com',
        )
        internship = create_internship(self.student, self.company)
        create_notification(other_admin, internship)

        res = self.client.get(NOTIFICATION_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    @patch('administration.views.generate_internship_agreement')
    def test_validate_marks_notification_as_read(self, mock_generate_agreement):
        """Validating an internship auto-marks related notifications as read."""
        internship = create_internship(self.student, self.company)
        notification = create_notification(self.admin_user, internship)

        self.client.patch(internship_validate_url(internship.id))

        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
        mock_generate_agreement.assert_called_once_with(
            internship, admin=self.admin_user,
        )

    def test_reject_marks_notification_as_read(self):
        """Rejecting an internship auto-marks related notifications as read."""
        internship = create_internship(self.student, self.company)
        notification = create_notification(self.admin_user, internship)

        self.client.patch(internship_reject_url(internship.id))

        notification.refresh_from_db()
        self.assertTrue(notification.is_read)


class AdminInternshipAgreementTests(TestCase):
    """Test internship agreement detail and download endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.university = create_university()
        self.admin_user = create_admin_user(self.university)
        self.student = create_student(self.university)
        self.company = create_company()
        self.internship = create_internship(self.student, self.company)
        self.client.force_authenticate(user=self.admin_user)

    def test_internship_detail_includes_agreement_metadata(self):
        agreement = create_internship_agreement(self.internship)

        res = self.client.get(internship_detail_url(self.internship.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('agreement', res.data)
        self.assertEqual(res.data['agreement']['id'], agreement.id)
        self.assertIn('/uploads/agreements/', res.data['agreement']['pdf_url'])
        self.assertTrue(res.data['agreement']['pdf_url'].endswith('.pdf'))
        self.assertIsNotNone(res.data['agreement']['generated_at'])

    def test_download_internship_agreement(self):
        create_internship_agreement(self.internship)

        res = self.client.get(internship_agreement_download_url(self.internship.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res['Content-Type'], 'application/pdf')
        self.assertIn(
            'attachment; filename="internship_agreement_',
            res['Content-Disposition'],
        )

    def test_download_internship_agreement_not_found(self):
        res = self.client.get(internship_agreement_download_url(self.internship.id))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_download_internship_agreement_forbidden_for_other_university(self):
        create_internship_agreement(self.internship)
        other_university = create_university(name='Other University', code='OTH')
        other_admin = create_admin_user(
            other_university,
            email='otheradmin@example.com',
        )
        self.client.force_authenticate(user=other_admin)

        res = self.client.get(internship_agreement_download_url(self.internship.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

