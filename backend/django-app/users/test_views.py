from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib import auth
from rest_framework import status
from .models import UserAccount
from .views import RegisterView, RetrieveUserView, GetCSRFTokenView, LoginView, LogoutView, CheckAuthenticatedView


class GetCSRFTokenViewTests(APITestCase):

    def test_request_response_status(self):
        '''
        Ensure response has correct status
        '''
        url = reverse('get-csrf-token')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_response_cookie(self):
        '''
        Ensure response contains csrf token
        '''
        url = reverse('get-csrf-token')
        response = self.client.get(url)
        self.assertIsNotNone(response.cookies['csrftoken'])


class RegisterViewTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.register_url = reverse('register')

        cls.default_user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'username': 'validuser',
            'password': 'validUserGoodPass852'
        }
        UserAccount.objects.create_user(**cls.default_user_data)

    def setUp(self):
        self.user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@test.com',
            'username': 'testuser',
            'password': 'TestUserGoodPass852'
        }


    def test_register_with_valid_info(self):
        '''
        Ensure registration successful for valid info
        '''
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserAccount.objects.count(), 2)

        user = UserAccount.objects.get(first_name=self.user_data['first_name'])
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))


    def test_bad_request_for_existing_user(self):
        '''
        Ensure registration fails for an existing user info
        '''
        response = self.client.post(self.register_url, self.default_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['email'][0]),
            'user account with this email already exists.',
        )
        self.assertEqual(
            str(response.data['username'][0]),
            'user account with this username already exists.',
        )
        self.assertEqual(UserAccount.objects.count(), 1)

    def test_bad_request_for_empty_first_name(self):
        '''
        Ensure registration fails for missing first name field
        '''
        self.user_data['first_name'] = ''
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['first_name']), 1)
        self.assertEqual(
            str(response.data['first_name'][0]),
            'This field may not be blank.',
        )
        self.assertEqual(UserAccount.objects.count(), 1)

    def test_bad_request_for_empty_last_name(self):
        '''
        Ensure registration fails for missing last name field
        '''
        self.user_data['last_name'] = ''
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['last_name']), 1)
        self.assertEqual(
            str(response.data['last_name'][0]),
            'This field may not be blank.',
        )
        self.assertEqual(UserAccount.objects.count(), 1)
    
    def test_bad_request_for_empty_password(self):
        '''
        Ensure registration fails for missing password field
        '''
        self.user_data['password'] = ''
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['password']), 1)
        self.assertEqual(
            str(response.data['password'][0]),
            'This field may not be blank.',
        )
        self.assertEqual(UserAccount.objects.count(), 1)

    def test_bad_request_for_short_password(self):
        '''
        Ensure registration fails for too short password
        '''
        self.user_data['password'] = 'asdpvn'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['password']), 1)
        self.assertEqual(
            str(response.data['password'][0]),
            'This password is too short. It must contain at least 8 characters.',
        )
        self.assertEqual(UserAccount.objects.count(), 1)

    def test_bad_request_for_common_password(self):
        '''
        Ensure registration fails for common password
        '''
        self.user_data['password'] = 'password123'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['password']), 1)
        self.assertEqual(
            str(response.data['password'][0]),
            'This password is too common.',
        )
        self.assertEqual(UserAccount.objects.count(), 1)


class LoginViewTests(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.check_auth_url = reverse('check-auth')
        self.user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'username': 'validuser',
            'password': 'validUserGoodPass852'
        }
        self.credentials = {
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        }
        UserAccount.objects.create_user(**self.user_data)


    def test_user_starts_not_authenticated(self):
        '''
        Ensure user starts not authenticated (sanity)
        '''
        client_user = auth.get_user(self.client)
        self.assertFalse(client_user.is_authenticated)

        # Ensure check authenticated view matches
        auth_response = self.client.get(self.check_auth_url)
        self.assertEqual(auth_response.data['isAuthenticated'], 'false')

    def test_valid_login_successful(self):
        '''
        Ensure correct credentials succesfully logs in the user
        '''
        # Ensure correct response status
        response = self.client.post(self.login_url, {
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure correct response data
        self.assertEqual(
            str(response.data['success']),
            'User authenticated.',
        )

        # Ensure user authenticated in backend
        auth_response = self.client.get(self.check_auth_url)
        self.assertEqual(auth_response.data['isAuthenticated'], 'true')

    def test_bad_request_incorrect_password(self):
        '''
        Ensure login fails for incorrect password
        '''
        # Ensure correct response status
        response = self.client.post(self.login_url, {
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Ensure correct response data
        self.assertEqual(
            str(response.data['error']),
            'Invalid credentials.',
        )

        # Ensure user not authenticated in backend
        auth_response = self.client.get(self.check_auth_url)
        self.assertEqual(auth_response.data['isAuthenticated'], 'false')

    def test_bad_request_no_matching_user(self):
        '''
        Ensure login fails for email not matching an existing user
        '''
        # Ensure correct response status
        response = self.client.post(self.login_url, {
            'email': 'nouser@test.com',
            'password': 'validUserGoodPass'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Ensure correct response data
        self.assertEqual(
            str(response.data['error']),
            'Invalid credentials.',
        )

    def test_bad_request_no_email(self):
        '''
        Ensure login fails for no email provided
        '''
        # Ensure correct response status
        response = self.client.post(self.login_url, {
            'email': '',
            'password': 'validUserGoodPass'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Ensure correct response data
        self.assertEqual(
            str(response.data['error']),
            'Invalid credentials.',
        )

    def test_bad_request_no_password(self):
        '''
        Ensure login fails for no password provided
        '''
        # Ensure successful response status
        response = self.client.post(self.login_url, {
            'email': 'nouser@test.com',
            'password': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Ensure successful response data
        self.assertEqual(
            str(response.data['error']),
            'Invalid credentials.',
        )

    
class CheckAuthenticatedViewTests(APITestCase):

    def setUp(self):
        self.check_auth_url = reverse('check-auth')
        self.user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'username': 'validuser',
            'password': 'validUserGoodPass852'
        }
        self.credentials = {
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        }
        UserAccount.objects.create_user(**self.user_data)

    def test_default_not_authenticated(self):
        '''
        Ensure user starts not authenticated
        '''
        auth_response = self.client.get(self.check_auth_url)
        self.assertEqual(auth_response.data['isAuthenticated'], 'false')

        # Verify user is actually not authenticated
        client_user = auth.get_user(self.client)
        self.assertFalse(client_user.is_authenticated)

    def test_authenticated_when_logged_in(self):
        '''
        Ensure view correctly verifies that user is authenticated
        '''
        self.client.login(**self.credentials)
        auth_response = self.client.get(self.check_auth_url)
        self.assertEqual(auth_response.data['isAuthenticated'], 'true')

        # Verify user is actually authenticated
        client_user = auth.get_user(self.client)
        self.assertTrue(client_user.is_authenticated)


class RetrieveUserViewTests(APITestCase):

    def setUp(self):
        self.whoami_url = reverse('current-user')
        self.user_account = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'username': 'validuser',
            'password': 'validUserGoodPass852'
        }
        self.user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'username': 'validuser'
        }
        self.credentials = {
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        }
        UserAccount.objects.create_user(**self.user_account)

    def test_unathenticated_fails(self):
        '''
        Ensure client is unable to access view without authenticated credentials
        '''
        response = self.client.get(self.whoami_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_authenticated_successful(self):
        '''
        Ensure view successfully returns user info for authenticated user
        '''
        self.client.login(**self.credentials)
        response = self.client.get(self.whoami_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data, self.user_data) # Ensure returns user data


class LogoutViewTests(APITestCase):

    def setUp(self):
        self.logout_url = reverse('logout')
        self.user_account = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'username': 'validuser',
            'password': 'validUserGoodPass852'
        }
        self.credentials = {
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        }
        UserAccount.objects.create_user(**self.user_account)

    def test_unathenticated_fails(self):
        '''
        Ensure client is unable to access view without authenticated credentials
        '''
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_authenticated_successful(self):
        '''
        Ensure view successfully returns user info for authenticated user
        '''
        self.client.login(**self.credentials)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Logged out successfully.')

        # Ensure user is logged out in backend
        client_user = auth.get_user(self.client)
        self.assertFalse(client_user.is_authenticated)
        
