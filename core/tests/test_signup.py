from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class PatientSignUpTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')  # Ensure you have named your URL in urls.py

    # def test_signup_valid(self):
    #     """
    #     Ensure we can create a new user and patient with valid data.
    #     """
    #     data = {
    #         'fallnumber': '123',
    #         'username': 'newuser2',
    #         'password': 'newpassword123',
    #         'email': 'user2@example.com',
    #         'birthday': '1990-10-10',
    #         'mobile_number': '1234567890'
    #     }
    #     response = self.client.post(self.signup_url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertIn('token', response.data)
    #     self.assertEqual(User.objects.count(), 1)
    #     self.assertEqual(Token.objects.count(), 1)

    def test_signup_invalid_user_data(self):
        """
        Ensure user data is validated.
        """
        data = {
            'username': 'newuser',  # Missing password and email
            'birthday': '2000-01-01',
            'mobile_number': '1234567890'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_signup_invalid_patient_data(self):
        """
        Ensure patient data is validated and no user is created if patient data is invalid.
        """
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'user@example.com',
            'birthday': 'not-a-date',  # Invalid date format
            'mobile_number': '1234567890'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

