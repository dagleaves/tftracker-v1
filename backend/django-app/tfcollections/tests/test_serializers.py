from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from tfcollections.models import Collection, CollectionItem
from transformers.models import Transformer, Toyline, Subline
from tfcollections.serializers import CollectionListSerializer, CollectionSerializer

class CollectionListSerializerTests(TestCase):

    def setUp(self):
        user_model = get_user_model()
        default_user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'username': 'validuser',
            'password': 'validUserGoodPass852'
        }
        self.user = user_model.objects.create_user(**default_user_data)
        self.collection = self.user.collections.get(name='Collection')
        
        # Create a sample transformer for testing
        self.def_toyline = Toyline.objects.create(name='None')
        self.def_subline = Subline.objects.create(name='None', toyline=self.def_toyline)
        self.transformer = Transformer.objects.create(
            picture=None,
            name='TF', 
            release_date=timezone.now(),
            price=0.0,
            toyline=self.def_toyline,
            subline=self.def_subline,
            size_class='Size Class',
            description='Description',
            manufacturer='H'
        )


    def test_setup(self):
        pass

    def test_length_empty(self):
        '''
        Ensure serializer method field 0 when collection is empty
        '''
        serializer = CollectionListSerializer(self.collection)
        length = serializer.data['length']
        self.assertEqual(length, 0)

    def test_length_nonempty(self):
        '''
        Ensure serializer method field populates as expected
        '''
        item = CollectionItem.objects.create(
            collection=self.collection, 
            transformer=self.transformer
        )
        
        serializer = CollectionListSerializer(self.collection)
        length = serializer.data['length']
        self.assertEqual(length, 1)
        


class CollectionSerializerTests(TestCase):

    def setUp(self):
        user_model = get_user_model()
        default_user_data = {
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@test.com',
            'username': 'validuser',
            'password': 'validUserGoodPass852'
        }
        self.user = user_model.objects.create_user(**default_user_data)
        self.collection = self.user.collections.get(name='Collection')
        
        # Create a sample transformer for testing
        self.def_toyline = Toyline.objects.create(name='None')
        self.def_subline = Subline.objects.create(name='None', toyline=self.def_toyline)
        self.transformer = Transformer.objects.create(
            picture=None,
            name='TF', 
            release_date=timezone.now(),
            price=0.0,
            toyline=self.def_toyline,
            subline=self.def_subline,
            size_class='Size Class',
            description='Description',
            manufacturer='H'
        )


    def test_setup(self):
        pass

    def test_length_empty(self):
        '''
        Ensure serializer method field 0 when collection is empty
        '''
        serializer = CollectionSerializer(self.collection)
        length = serializer.data['length']
        self.assertEqual(length, 0)

    def test_length_nonempty(self):
        '''
        Ensure serializer method field populates as expected
        '''
        item = CollectionItem.objects.create(
            collection=self.collection, 
            transformer=self.transformer
        )
        
        serializer = CollectionSerializer(self.collection)
        length = serializer.data['length']
        self.assertEqual(length, 1)

    def test_items_empty(self):
        '''
        Ensure serializer items field is empty with no items
        '''
        serializer = CollectionSerializer(self.collection)
        items = serializer.data['items']
        self.assertEqual(len(items), 0)

    def test_items_nonempty(self):
        '''
        Ensure serializer items field populates as expected
        '''
        CollectionItem.objects.create(
            collection=self.collection, 
            transformer=self.transformer
        )
        
        serializer = CollectionSerializer(self.collection)
        items = serializer.data['items']
        self.assertEqual(len(items), 1)
        