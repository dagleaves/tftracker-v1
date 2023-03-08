from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from tfcollections.models import Collection, CollectionItem
from transformers.models import Transformer, Toyline, Subline

class CollectionModelTests(TestCase):

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
        Collection.objects.create(user=self.user, name='Custom', public=False)

    def test_setup(self):
        pass

    def test_sanity(self):
        '''
        Ensure model fields behave as expected
        '''
        collections = self.user.collections.all()
        owned = collections.filter(name='Collection')
        wishlist = collections.filter(name='Wishlist')
        custom = collections.filter(name='Custom')
        self.assertEqual(collections.count(), 3)
        self.assertEqual(owned.count(), 1)
        self.assertEqual(wishlist.count(), 1)
        self.assertEqual(custom.count(), 1)
        self.assertTrue(owned[0].public)
        self.assertTrue(wishlist[0].public)
        self.assertFalse(custom[0].public)


class CollectionItemTests(TestCase):

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

    def test_sanity(self):
        '''
        Ensure model fields behave as expected
        '''
        item = CollectionItem.objects.create(
            collection=self.collection, 
            transformer=self.transformer
        )

        collections = self.user.collections.all()
        owned = collections.filter(name='Collection')
        wishlist = collections.filter(name='Wishlist')
        self.assertEqual(collections.count(), 2)
        self.assertEqual(owned.count(), 1)
        self.assertEqual(wishlist.count(), 1)
        self.assertTrue(owned[0].public)
        self.assertTrue(wishlist[0].public)
        self.assertEqual(owned[0], self.collection)
        
        # Ensure item added correctly
        items = self.collection.items.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0], item)
