from django.contrib.auth.models import User
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.serializers import UserSerializer
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from users.views import LogoutView, DeleteUserView
from rest_framework.test import APIRequestFactory, force_authenticate

from joblib import load



class RegisterViewTest(APITestCase):

    def test_register_user(self):
        url = reverse('register')

        data = {
            "first_name": "testuser",
            "last_name": "testuser",
            "email": "testuser@testuser.com",
            "password": "1a2s3d4f"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)





class LoginViewTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@testuser.com',
            password='testpassword'
        )

    def test_login_user(self):

        url = reverse('login')
        data = {
            'email': 'testuser@testuser.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)
        self.assertEqual(response.data['email'], 'testuser@testuser.com')








class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = APIRequestFactory()

    def test_logout_view(self):
        request = self.factory.post('/logout/')
        response = LogoutView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Logout success!'})
        self.assertTrue('jwt' in response.cookies)
        self.assertEqual(response.cookies['jwt'].value, '')






class DeleteUserViewTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(

            email='testuser@test.com',
            password='testpass123',

        )
        self.token = Token.objects.create(user=self.user)

    def test_delete_user_view(self):
        url = reverse('delete_user', kwargs={'email': self.user.email})
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user, token=self.token)
        response = DeleteUserView.as_view()(request, email=self.user.email)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(get_user_model().objects.filter(email=self.user.email).exists())


class PredictorTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email='testuser@testuser.com', password='testpass'
        )

        self.url = reverse('predictor')

        self.data = {
            'sepal_length': 5.1,
            'sepal_width': 3.5,
            'petal_length': 1.4,
            'petal_width': 0.2,
        }

    def test_predictor_view(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('result', response.data)