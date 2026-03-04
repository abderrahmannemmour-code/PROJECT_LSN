"""Tests for the administration API."""
from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    University,
    Student,
    Company,
    Admin,
    Internship,
)


INTERNSHIP_LIST_URL = reverse('administration:internship-list')
INTERNSHIP_PENDING_URL = reverse('administration:internship-pending')


def internship_detail_url(internship_id):
    return reverse('administration:internship-detail', args=[internship_id])


def internship_validate_url(internship_id):
    return reverse('administration:internship-validate', args=[internship_id])


def internship_reject_url(internship_id):
    return reverse('administration:internship-reject', args=[internship_id])


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


class PublicAdministrationApiTests(TestCase):
    """Test unauthenticated access is denied."""

    def setUp(self):
        self.client = APIClient()

    def test_internship_list_requires_auth(self):
        res = self.client.get(INTERNSHIP_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pending_list_requires_auth(self):
        res = self.client.get(INTERNSHIP_PENDING_URL)
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

    def test_list_pending_internships(self):
        """Only accepted_by_company internships appear in pending list."""
        create_internship(self.student, self.company)
        create_internship(
            self.student, self.company,
            status=Internship.Status.PENDING,
        )

        res = self.client.get(INTERNSHIP_PENDING_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(
            res.data[0]['status'], Internship.Status.ACCEPTED_BY_COMPANY,
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

    def test_validate_internship(self):
        internship = create_internship(self.student, self.company)

        res = self.client.patch(internship_validate_url(internship.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        internship.refresh_from_db()
        self.assertEqual(internship.status, Internship.Status.VALIDATED)

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

