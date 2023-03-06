from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from tfcollections.models import Collection


class MyCollectionsViewTests(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_model = get_user_model()
        cls.default_user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        }
        cls.other_user_data = {
            'first_name': 'Other',
            'last_name': 'User',
            'email': 'otheruser@test.com',
            'password': 'validUserGoodPass852'
        }
        cls.user = cls.user_model.objects.create_user(**cls.default_user_data)
        cls.other_user = cls.user_model.objects.create_user(**cls.other_user_data)
        cls.user_pk = cls.user.id
        cls.url = reverse('my-collections-list')


    def setUp(self):
        self.client.force_authenticate(user=self.user)


    def test_setup(self):
        pass


    def test_default_lists(self):
        '''
        Ensure user returns empty default collections
        '''
        response = self.client.get(self.url)
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)


    def test_new_collection(self):
        '''
        Ensure non-default collections return correctly
        '''
        Collection.objects.create(
            user=self.user,
            name='Custom',
            public=True
        )

        response = self.client.get(self.url)
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 3)


    def test_private_collection(self):
        '''
        Ensure private collections are returned for current user
        '''
        Collection.objects.create(
            user=self.user,
            name='Custom',
            public=False
        )

        response = self.client.get(self.url)
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 3)

    
    def test_non_current_user_private_collection(self):
        '''
        Ensure private collections from other users are not returned
        '''
        Collection.objects.create(
            user=self.other_user,
            name='Custom',
            public=False
        )

        response = self.client.get(self.url)
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)


class MyCollectionViewTests(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_model = get_user_model()
        cls.default_user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        }
        cls.other_user_data = {
            'first_name': 'Other',
            'last_name': 'User',
            'email': 'otheruser@test.com',
            'password': 'validUserGoodPass852'
        }
        cls.user = cls.user_model.objects.create_user(**cls.default_user_data)
        cls.other_user = cls.user_model.objects.create_user(**cls.other_user_data)
        cls.user_pk = cls.user.id


    def setUp(self):
        self.client.force_authenticate(user=self.user)


    def test_setup(self):
        pass


    def test_bad_request(self):
        '''
        Ensure invalid pk returns not found
        '''
        url = reverse('my-collection', kwargs={'pk': 12345})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_default_collection(self):
        '''
        Ensure default collection returns correctly
        '''
        pk = Collection.objects.get(user=self.user, name='Collection').id
        url = reverse('my-collection', kwargs={'pk': pk})
        response = self.client.get(url)
        results = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 4)
        self.assertEqual(results['name'], 'Collection')


    def test_new_collection(self):
        '''
        Ensure non-default collections return correctly
        '''
        new_collection = Collection.objects.create(
            user=self.user,
            name='Custom',
            public=True
        )

        pk = new_collection.id
        url = reverse('my-collection', kwargs={'pk': pk})
        response = self.client.get(url)
        results = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 4)
        self.assertEqual(results['name'], 'Custom')


    def test_private_collection(self):
        '''
        Ensure private collections are returned for current user
        '''
        new_collection = Collection.objects.create(
            user=self.user,
            name='Custom',
            public=False
        )

        pk = new_collection.id
        url = reverse('my-collection', kwargs={'pk': pk})
        response = self.client.get(url)
        results = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 4)
        self.assertEqual(results['name'], 'Custom')

    
    def test_non_current_user_private_collection(self):
        '''
        Ensure private collections from other users are not returned
        '''
        new_collection = Collection.objects.create(
            user=self.other_user,
            name='Custom',
            public=False
        )

        pk = new_collection.id
        url = reverse('my-collection', kwargs={'pk': pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PublicCollectionsViewTests(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_model = get_user_model()
        cls.default_user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        }
        cls.other_user_data = {
            'first_name': 'Other',
            'last_name': 'User',
            'email': 'otheruser@test.com',
            'password': 'validUserGoodPass852'
        }
        cls.user = cls.user_model.objects.create_user(**cls.default_user_data)
        cls.other_user = cls.user_model.objects.create_user(**cls.other_user_data)
        cls.user_pk = cls.user.id
        cls.other_user_pk = cls.other_user.id


    def setUp(self):
        self.client.force_authenticate(user=self.user)


    def test_setup(self):
        pass


    def test_current_user_default_lists(self):
        '''
        Ensure user returns empty default collections
        '''
        url = reverse('public-collections-list', kwargs={'pk': self.user_pk})
        response = self.client.get(url)
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)


    def test_other_user_default_lists(self):
        '''
        Ensure other user returns empty default collections
        '''
        url = reverse('public-collections-list', kwargs={'pk': self.other_user_pk})
        response = self.client.get(url)
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)


    def test_current_user_new_collection(self):
        '''
        Ensure current user non-default collections return correctly
        '''
        Collection.objects.create(
            user=self.user,
            name='Custom',
            public=True
        )

        url = reverse('public-collections-list', kwargs={'pk': self.user_pk})
        response = self.client.get(url)
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 3)


    def test_other_user_new_collection(self):
        '''
        Ensure other user non-default collections return correctly
        '''
        Collection.objects.create(
            user=self.other_user,
            name='Custom',
            public=True
        )

        url = reverse('public-collections-list', kwargs={'pk': self.other_user_pk})
        response = self.client.get(url)
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 3)


    def test_current_user_private_collection(self):
        '''
        Ensure private collections are NOT returned for current user
        '''
        Collection.objects.create(
            user=self.user,
            name='Custom',
            public=False
        )

        url = reverse('public-collections-list', kwargs={'pk': self.user_pk})
        response = self.client.get(url)
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)

    
    def test_other_user_private_collection(self):
        '''
        Ensure private collections from other users are not returned
        '''
        Collection.objects.create(
            user=self.other_user,
            name='Custom',
            public=False
        )

        url = reverse('public-collections-list', kwargs={'pk': self.other_user_pk})
        response = self.client.get(url)
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2)


class PublicCollectionViewTests(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_model = get_user_model()
        cls.default_user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        }
        cls.other_user_data = {
            'first_name': 'Other',
            'last_name': 'User',
            'email': 'otheruser@test.com',
            'password': 'validUserGoodPass852'
        }
        cls.user = cls.user_model.objects.create_user(**cls.default_user_data)
        cls.other_user = cls.user_model.objects.create_user(**cls.other_user_data)
        cls.user_pk = cls.user.id


    def setUp(self):
        self.client.force_authenticate(user=self.user)


    def test_setup(self):
        pass


    def test_bad_request(self):
        '''
        Ensure invalid pk returns not found
        '''
        url = reverse('public-collection', kwargs={'pk': 12345})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_other_user_default_collection(self):
        '''
        Ensure other user default collection returns correctly
        '''
        pk = Collection.objects.get(user=self.other_user, name='Collection').id
        url = reverse('public-collection', kwargs={'pk': pk})
        response = self.client.get(url)
        results = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 4)
        self.assertEqual(results['name'], 'Collection')


    def test_other_user_new_collection(self):
        '''
        Ensure other user non-default collections return correctly
        '''
        new_collection = Collection.objects.create(
            user=self.other_user,
            name='Custom',
            public=True
        )

        pk = new_collection.id
        url = reverse('public-collection', kwargs={'pk': pk})
        response = self.client.get(url)
        results = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 4)
        self.assertEqual(results['name'], 'Custom')


    def test_current_user_default_collection(self):
        '''
        Ensure current user default collection still returns correctly
        '''
        pk = Collection.objects.get(user=self.user, name='Collection').id
        url = reverse('public-collection', kwargs={'pk': pk})
        response = self.client.get(url)
        results = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 4)
        self.assertEqual(results['name'], 'Collection')


    def test_current_user_new_collection(self):
        '''
        Ensure current user non-default collections return correctly
        '''
        new_collection = Collection.objects.create(
            user=self.user,
            name='Custom',
            public=True
        )

        pk = new_collection.id
        url = reverse('public-collection', kwargs={'pk': pk})
        response = self.client.get(url)
        results = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 4)
        self.assertEqual(results['name'], 'Custom')


    def test_current_user_private_collection(self):
        '''
        Ensure private collections are NOT returned for current user
        '''
        new_collection = Collection.objects.create(
            user=self.user,
            name='Custom',
            public=False
        )

        pk = new_collection.id
        url = reverse('public-collection', kwargs={'pk': pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_other_user_private_collection(self):
        '''
        Ensure private collections from other users are NOT returned
        '''
        new_collection = Collection.objects.create(
            user=self.other_user,
            name='Custom',
            public=False
        )

        pk = new_collection.id
        url = reverse('public-collection', kwargs={'pk': pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)