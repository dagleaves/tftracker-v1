from django.test import TestCase
from .models import UserAccount
from .serializers import UserRegistrationSerializer, UserSerializer

# Create your tests here.

class UserRegistrationSerializerTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

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
        self.serializer = UserRegistrationSerializer(data=self.user_data)
        self.is_valid = self.serializer.is_valid()


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
        user = self.serializer.validated_data
        self.assertEqual(user['first_name'], self.user_data['first_name'])
        self.assertEqual(user['last_name'], self.user_data['last_name'])
        self.assertEqual(user['email'], self.user_data['email'])
        self.assertEqual(user['username'], self.user_data['username'])
    
    def test_user_data_matches(self):
        self.serializer.create(self.serializer.validated_data)
        user = UserAccount.objects.get(first_name='Test')
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
        self.user_data['username'] = 'othervalidusername'
        self.user_data['email'] = self.default_user_data['email']
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

    def test_empty_username_invalid(self):
        self.user_data['username'] = ''
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
    
    def test_existing_username_invalid(self):
        self.user_data['username'] = self.default_user_data['username']
        self.user_data['email'] = 'othervalid@email.com'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_short_username_invalid(self):
        self.user_data['username'] = 'abc'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
    
    def test_username_symbols_invalid(self):
        self.user_data['username'] = '@test.com'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_numeric_username_valid(self):
        self.user_data['username'] = '12345'
        serializer = UserRegistrationSerializer(data=self.user_data)
        serializer.is_valid()

    def test_username_startswith_hyphen_invalid(self):
        self.user_data['username'] = '-invalidusername'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_username_endswith_hypen_invalid(self):
        self.user_data['username'] = 'invalid-'
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_username_double_hypen_invalid(self):
        self.user_data['username'] = 'invalid--invalid'
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
            'username': 'testuser',
            'password': 'TestUserGoodPass852'
        } 
        self.serializer = UserRegistrationSerializer(data=self.user_data)
        self.serializer.is_valid()
        self.user = self.serializer.create(self.serializer.validated_data)
        self.user_serializer = UserSerializer(self.user)

    def test_keys_match(self):
        self.assertCountEqual(self.user_serializer.data.keys(), ['first_name', 'last_name', 'email', 'username'])

    def test_values_match(self):
        self.assertCountEqual(self.user_serializer.data.values(), ['Test', 'User', 'testuser@test.com', 'testuser'])