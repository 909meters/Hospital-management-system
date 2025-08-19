from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from .models import CustomUser
from rest_framework.test import APITestCase


class DoctorListAPITest(APITestCase):
    def setUp(self):
        self.doctor = CustomUser.objects.create_user(
            username='testdoctor',
            password='password123',
            first_name='John',
            last_name='Doe',
            role='DOCTOR'
        )
        self.patient = CustomUser.objects.create_user(
            username='testpatient',
            password='password123',
            role='PATIENT'
        )
        self.url = reverse('doctor-list')

    def test_doctor_can_access_doctor_list(self):
        self.client.force_authenticate(user=self.doctor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], self.doctor.username)

    def test_patient_cannot_access_doctor_list(self):
        self.client.force_authenticate(user=self.patient)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)