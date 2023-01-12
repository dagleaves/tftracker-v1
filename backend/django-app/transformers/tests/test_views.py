from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from transformers.models import Transformer, Toyline, Subline

import os
import shutil
import datetime


class TransformerListViewTests(APITestCase):

    def_toyline, _ = Toyline.objects.get_or_create(name='None')
    def_subline, _ = Subline.objects.get_or_create(name='None', defaults={'toyline': def_toyline})
    def create_default_transformer(self, picture=None, name="Bumblebee", release_date=timezone.now().date(), price=19.99, toyline=def_toyline, subline=def_subline, size_class='Deluxe', description="", manufacturer='H'):
        if picture is None:
            picture = SimpleUploadedFile(name='foo.gif', 
                    content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00')
        if toyline is None:
            toyline = self.def_toyline
        if subline is None:
            subline = self.def_subline
        tf = Transformer.objects.create(picture=picture, name=name, release_date=release_date, price=price, toyline=toyline, subline=subline, size_class=size_class, description=description, manufacturer=manufacturer)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        def_toyline, _ = Toyline.objects.get_or_create(name='None')
        def_subline, _ = Subline.objects.get_or_create(name='None', defaults={'toyline': def_toyline})
        cls.user_model = get_user_model()
        cls.default_user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        }
        cls.user = cls.user_model.objects.create_user(**cls.default_user_data)
        cls.url = reverse('list-view') 

    def setUp(self):
        self.client.force_authenticate(user=self.user)
        self.generations, _ = Toyline.objects.get_or_create(name='Generations')
        self.studio_series, _ = Subline.objects.get_or_create(toyline=self.generations, name='Studio Series')
        self.legacy, _ = Subline.objects.get_or_create(toyline=self.generations, name='Legacy')
        self.earthspark, _ = Toyline.objects.get_or_create(name='EarthSpark')

    def tearDown(self):
        shutil.rmtree('media', ignore_errors=True)
        os.mkdir('media')


    def test_no_transformers_returns_empty(self):
        '''
        Ensure empty database returns no results
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['count'], 0)
    
    def test_one_transformer_returns_correctly(self):
        '''
        Ensure one entry only returns one entry
        '''
        
        self.create_default_transformer(toyline=self.generations, subline=self.studio_series)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['count'], 1)

    def test_multiple_transformers_returns_correctly(self):
        '''
        Ensure multiple entries returns in correct order
        '''
        self.create_default_transformer(toyline=self.generations, subline=self.studio_series)
        self.create_default_transformer(name='Skywarp Autobot Multiple Words', toyline=self.generations, subline=self.studio_series)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], 'Bumblebee')
        self.assertEqual(response.data['results'][1]['name'], 'Skywarp Autobot Multiple Words')


class TransformerDetailViewTests(APITestCase):

    def_toyline, _ = Toyline.objects.get_or_create(name='None')
    def_subline, _ = Subline.objects.get_or_create(name='None', defaults={'toyline': def_toyline})
    def create_default_transformer(self, picture=None, name="Bumblebee", release_date=timezone.now().date(), price=19.99, toyline=def_toyline, subline=def_subline, size_class='Deluxe', description="", manufacturer='H'):
        if picture is None:
            picture = SimpleUploadedFile(name='foo.gif', 
                    content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00')
        if toyline is None:
            toyline = self.def_toyline
        if subline is None:
            subline = self.def_subline
        tf = Transformer.objects.create(picture=picture, name=name, release_date=release_date, price=price, toyline=toyline, subline=subline, size_class=size_class, description=description, manufacturer=manufacturer)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        def_toyline, _ = Toyline.objects.get_or_create(name='None')
        def_subline, _ = Subline.objects.get_or_create(name='None', defaults={'toyline': def_toyline})
        cls.user_model = get_user_model()
        cls.default_user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        }
        cls.user = cls.user_model.objects.create_user(**cls.default_user_data)

    def setUp(self):
        self.generations, _ = Toyline.objects.get_or_create(name='Generations')
        self.studio_series, _ = Subline.objects.get_or_create(toyline=self.generations, name='Studio Series')
        self.legacy, _ = Subline.objects.get_or_create(toyline=self.generations, name='Legacy')
        self.earthspark, _ = Toyline.objects.get_or_create(name='EarthSpark')
        self.client.force_authenticate(user=self.user)
        self.create_default_transformer(toyline=self.generations, subline=self.studio_series)

    def tearDown(self):
        shutil.rmtree('media', ignore_errors=True)
        os.mkdir('media')


    def test_bad_request_invalid_transformer(self):
        '''
        Ensure a non-existant pk returns a bad request
        '''
        url = reverse('detail-view', args=('-1',))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_one_transformer_returns_correctly(self):
        '''
        Ensure detail view returns correct information for valid pk
        '''
        tf = Transformer.objects.get(name='Bumblebee')
        url = reverse('detail-view', args=(tf.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        tf = Transformer.objects.get(name='Bumblebee')
        self.assertEqual(tf.name, data['name'])
        self.assertTrue(data['picture'].endswith(tf.picture.url))
        self.assertEqual(str(tf.release_date), data['release_date'])
        self.assertEqual(tf.price, data['price'])
        self.assertEqual(tf.toyline.name, data['toyline'])
        self.assertEqual(tf.subline.name, data['subline'])
        self.assertEqual(tf.size_class, data['size_class'])
        self.assertEqual(tf.description, data['description'])
        self.assertEqual(tf.manufacturer, data['manufacturer'])
        self.assertTrue(tf.is_visible)


class TransformerSearchViewTests(APITestCase):
    
    def_toyline, _ = Toyline.objects.get_or_create(name='None')
    def_subline, _ = Subline.objects.get_or_create(name='None', defaults={'toyline': def_toyline})
    def create_default_transformer(self, picture=None, name="Bumblebee", release_date=timezone.now().date(), price=19.99, toyline=None, subline=None, size_class='Deluxe', description="", manufacturer='H'):
        if picture is None:
            picture = SimpleUploadedFile(name='foo.gif', 
                    content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00')
        if toyline is None:
            toyline = self.def_toyline
        if subline is None:
            subline = self.def_subline
        tf = Transformer.objects.create(picture=picture, name=name, release_date=release_date, price=price, toyline=toyline, subline=subline, size_class=size_class, description=description, manufacturer=manufacturer)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        def_toyline, _ = Toyline.objects.get_or_create(name='None')
        def_subline, _ = Subline.objects.get_or_create(name='None', defaults={'toyline': def_toyline})
        cls.user_model = get_user_model()
        cls.default_user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'password': 'validUserGoodPass852'
        }
        cls.user = cls.user_model.objects.create_user(**cls.default_user_data)
        cls.url = reverse('search-view')

    def setUp(self):
        generations, _ = Toyline.objects.get_or_create(name='Generations')
        studio_series, _ = Subline.objects.get_or_create(name='Studio Series', defaults={'toyline': generations})
        legacy, _ = Subline.objects.get_or_create(name='Legacy', defaults={'toyline': generations})
        earthspark, _ = Toyline.objects.get_or_create(name='EarthSpark')
        self.client.force_authenticate(user=self.user)
        self.create_default_transformer(toyline=generations, subline=studio_series)
        self.create_default_transformer(name='Skywarp Autobot Multiple Words', toyline=generations, subline=studio_series)
        self.create_default_transformer(name='Optimus Prime', price=50.0, toyline=earthspark, release_date=(timezone.now().date() + datetime.timedelta(days=2)), description='TF', manufacturer='T')
        
        self.filters = {
            'toyline': '',
            'size_class': '',
            'manufacturer': '',
            'release_date': '',
            'future_releases': 'true',
            'price': '',
            'search': '',
        }

    def tearDown(self):
        shutil.rmtree('media', ignore_errors=True)
        os.mkdir('media')


    def test_defaults_return_all_in_database(self):
        response = self.client.post(self.url, self.filters)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    
    def test_filter_single_toyline_match(self):
        toyline = 'Generations'
        self.filters['toyline'] = toyline

        response = self.client.post(self.url, self.filters)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['toyline'], toyline)
        self.assertEqual(response.data[1]['toyline'], toyline)