from django.test import TestCase
from .models import UserAccount
from .serializers import UserRegistrationSerializer, UserSerializer

# Create your tests here.

class UserRegistrationSerializerTests(TestCase):

    def setUp(self):
        self.user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@test.com',
            'password': 'TestUserGoodPass852'
        } 
        self.serializer = UserRegistrationSerializer(data=self.user_data)
        self.is_valid = self.serializer.is_valid()
        self.user = self.serializer.create(self.serializer.validated_data)

    def test_data_is_valid(self):
        self.assertTrue(self.serializer.is_valid())
        
    def test_unvalidated_data_keys_match(self):
        self.assertCountEqual(self.serializer.data.keys(), self.user_data.keys())

    def test_validated_data_keys_match(self):
        self.assertCountEqual(self.serializer.validated_data.keys(), self.user_data.keys())

    def test_unvalidated_data_matches(self):
        self.assertCountEqual(self.serializer.data.values(), self.user_data.values())

    def test_validated_data_matches(self):
        self.assertCountEqual(self.serializer.validated_data.values(), self.user_data.values())

    def test_user_was_created(self):
        self.assertEqual(UserAccount.objects.count(), 1)
    
    def test_user_data_matches(self):
        user = UserAccount.objects.all()[0]
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_empty_first_name_invalid(self):
        self.user_data['first_name'] = ''
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_empty_last_name_invalid(self):
        self.user_data['last_name'] = ''
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_empty_email_invalid(self):
        self.user_data['email'] = ''
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
    
    def test_existing_email_invalid(self):
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_no_at_symbol_email_invalid(self):
        self.user_data['email'] = 'testemailtest.com'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
    
    def test_no_email_prefix_invalid(self):
        self.user_data['email'] = '@test.com'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_no_period_email_invalid(self):
        self.user_data['email'] = 'testemail@testcom'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_no_email_domain_name_invalid(self):
        self.user_data['email'] = 'testemail@.com'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_no_email_domain_invalid(self):
        self.user_data['email'] = 'testemail@'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_empty_password_invalid(self):
        self.user_data['password'] = ''
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_common_password_invalid(self):
        self.user_data['password'] = 'password123'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_short_password_invalid(self):
        self.user_data['password'] = 'pizza'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())


class UserSerializerTests(TestCase):

    def setUp(self):
        self.user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@test.com',
            'password': 'TestUserGoodPass852'
        } 
        self.serializer = UserRegistrationSerializer(data=self.user_data)
        self.serializer.is_valid()
        self.user = self.serializer.create(self.serializer.validated_data)
        self.user_serializer = UserSerializer(self.user)

    def test_keys_match(self):
        self.assertCountEqual(self.user_serializer.data.keys(), ['first_name', 'last_name', 'email'])

    def test_values_match(self):
        self.assertCountEqual(self.user_serializer.data.values(), ['Test', 'User', 'testuser@test.com'])