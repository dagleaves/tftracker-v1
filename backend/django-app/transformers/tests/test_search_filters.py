from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from django.urls import reverse

from transformers.models import Transformer, Toyline, Subline
from transformers.views import TransfomerSearchView

import os
import shutil
import datetime


class TransformerSearchViewFilterTests(APITestCase):

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
            'username': 'validuser',
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
        self.create_default_transformer(name='Skywarp Prime Multiple Words', toyline=generations, subline=studio_series)
        self.create_default_transformer(name='Optimus Prime', price=50.0, toyline=earthspark, release_date=(timezone.now().date() + datetime.timedelta(days=2)), description='TF', manufacturer='T')
        
        self.filters = {
            'search': '',
            'toyline': [],
            'subline': [],
            'size_class': [],
            'manufacturer': [],
            'release_date': [None, None],
            'future_releases': True,
            'price': [None, None],
            'order': '',
            'ascending': ''
        }
        self.view = TransfomerSearchView()

    def tearDown(self):
        shutil.rmtree('media', ignore_errors=True)
        os.mkdir('media')


    def test_setup(self):
        pass

    def test_filter_toyline_no_match(self):
        '''
        Ensure filter toyline method returns no entries for a non-matching toyline
        '''
        toyline = 'Invalid'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_toyline(queryset, toyline)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_toyline_matches(self):
        '''
        Ensure filter toyline method returns only matching toylines
        '''
        toylines = ['Generations']
        queryset = self.view.get_queryset()
        queryset = self.view.filter_toyline(queryset, toylines)
        results = list(queryset)

        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].toyline.name in toylines)
        self.assertTrue(results[1].toyline.name in toylines)

    def test_filter_toyline_multiple_toylines_matches(self):
        '''
        Ensure filter toyline method returns for multiple toylines to search for
        '''
        toylines = ['Generations', 'EarthSpark']
        queryset = self.view.get_queryset()
        queryset = self.view.filter_toyline(queryset, toylines)
        results = list(queryset)

        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].toyline.name in toylines)
        self.assertTrue(results[1].toyline.name in toylines)
        self.assertTrue(results[2].toyline.name in toylines)

    def test_filter_subline_no_match(self):
        '''
        Ensure filter subline method returns no entries for a non-matching subline
        '''
        subline = 'Invalid'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_subline(queryset, subline)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_subline_matches(self):
        '''
        Ensure filter subline method returns only matching toylines
        '''
        sublines = ['Studio Series']
        queryset = self.view.get_queryset()
        queryset = self.view.filter_subline(queryset, sublines)
        results = list(queryset)

        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].subline.name in sublines)
        self.assertTrue(results[1].subline.name in sublines)

    def test_filter_multiple_sublines_match(self):
        '''
        Ensure filter subline method returns for multiple sublines to search for, including None
        '''
        sublines = ['Studio Series', 'None']
        queryset = self.view.get_queryset()
        queryset = self.view.filter_subline(queryset, sublines)
        results = list(queryset)

        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].subline.name in sublines)
        self.assertTrue(results[1].subline.name in sublines)
        self.assertTrue(results[2].subline.name in sublines)

    def test_filter_size_class_no_match(self):
        '''
        Ensure size class filter method returns nothing for not matching size class
        '''
        size_class = 'Invalid'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_size_class(queryset, size_class)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_size_class_matches(self):
        '''
        Ensure size class filter returns only matching size classes
        '''
        size_class = 'Deluxe'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_size_class(queryset, size_class)
        results = list(queryset)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].size_class, size_class)
        self.assertEqual(results[1].size_class, size_class)

    def test_filter_multiple_size_class_matches(self):
        '''
        Ensure size class filter returns for multiple size classes in query
        '''
        size_classes = ['Deluxe', 'None']
        queryset = self.view.get_queryset()
        queryset = self.view.filter_size_class(queryset, size_classes)
        results = list(queryset)

        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].size_class in size_classes)
        self.assertTrue(results[1].size_class in size_classes)
        self.assertTrue(results[2].size_class in size_classes)

    def test_filter_manufacturer_no_match(self):
        '''
        Ensure manufacturer filter method returns no matches for not matching manufacturer
        '''
        manufacturer = 'Invalid'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_manufacturer(queryset, manufacturer)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_manufacturer_matches(self):
        '''
        Ensure manufacturer filter method returns no matches for not matching manufacturer
        '''
        manufacturer = 'H'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_manufacturer(queryset, manufacturer)
        results = list(queryset)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].manufacturer, manufacturer)
        self.assertEqual(results[1].manufacturer, manufacturer)

    def test_filter_size_class_matches(self):
        '''
        Ensure manufacturer filter returns for multiple manufacturers in query
        '''
        manufacturers = 'H,T'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_manufacturer(queryset, manufacturers)
        results = list(queryset)

        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].manufacturer in manufacturers)
        self.assertTrue(results[1].manufacturer in manufacturers)
        self.assertTrue(results[2].manufacturer in manufacturers)

    def test_filter_release_date_lower_bound_no_matches(self):
        '''
        Ensure release date filter method returns no matches for a high lower bound
        '''
        release_date_lower_bound = str(timezone.now().date() + datetime.timedelta(days=100))
        release_date_upper_bound = None
        release_date = [release_date_lower_bound, release_date_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_release_date(queryset, release_date)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_release_date_lower_bound_matches(self):
        '''
        Ensure release date filter method returns matches for a valid lower bound
        '''
        release_date_lower_bound = str(timezone.now().date())
        release_date_upper_bound = None
        release_date = [release_date_lower_bound, release_date_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_release_date(queryset, release_date)
        results = list(queryset)

        self.assertEqual(len(results), 3)
        self.assertGreaterEqual(results[0].release_date, timezone.now().date())
        self.assertGreaterEqual(results[1].release_date, timezone.now().date())
        self.assertGreaterEqual(results[2].release_date, timezone.now().date())

    def test_filter_release_date_upper_bound_no_matches(self):
        '''
        Ensure release date filter method returns no matches for a low upper bound
        '''
        release_date_lower_bound = None
        release_date_upper_bound = str(timezone.now().date() + datetime.timedelta(days=-100))
        release_date = [release_date_lower_bound, release_date_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_release_date(queryset, release_date)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_release_date_upper_bound_matches(self):
        '''
        Ensure release date filter method returns matches for a valid upper bound
        '''
        release_date_lower_bound = None
        release_date_upper_bound = str(timezone.now().date() + datetime.timedelta(days=100))
        release_date = [release_date_lower_bound, release_date_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_release_date(queryset, release_date)
        results = list(queryset)

        self.assertEqual(len(results), 3)
        self.assertGreaterEqual(results[0].release_date, timezone.now().date())
        self.assertGreaterEqual(results[1].release_date, timezone.now().date())
        self.assertGreaterEqual(results[2].release_date, timezone.now().date())

    def test_filter_release_date_range_no_matches(self):
        '''
        Ensure release date filter method returns no matches for no matching lower and upper bounds
        '''
        release_date_lower_bound = str(timezone.now().date() + datetime.timedelta(days=90))
        release_date_upper_bound = str(timezone.now().date() + datetime.timedelta(days=100))
        release_date = [release_date_lower_bound, release_date_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_release_date(queryset, release_date)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_release_date_range_matches(self):
        '''
        Ensure release date filter method returns matches for valid lower and upper bounds
        '''
        release_date_lower_bound = str(timezone.now().date() + datetime.timedelta(days=-100))
        release_date_upper_bound = str(timezone.now().date() + datetime.timedelta(days=100))
        release_date = [release_date_lower_bound, release_date_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_release_date(queryset, release_date)
        results = list(queryset)

        self.assertEqual(len(results), 3)
        self.assertGreaterEqual(results[0].release_date, timezone.now().date())
        self.assertGreaterEqual(results[1].release_date, timezone.now().date())
        self.assertGreaterEqual(results[2].release_date, timezone.now().date())

    def test_filter_no_future_releases(self):
        '''
        Ensure future release filter (false) returns only released figures
        '''
        future_releases = False
        queryset = self.view.get_queryset()
        queryset = self.view.filter_future_releases(queryset, future_releases)
        results = list(queryset)

        self.assertEqual(len(results), 2)
        self.assertLessEqual(results[0].release_date, timezone.now().date())
        self.assertLessEqual(results[1].release_date, timezone.now().date())

    def test_filter_future_releases_included(self):
        '''
        Ensure future release filter (true) returns all figures (including future releases)
        '''
        future_releases = True
        queryset = self.view.get_queryset()
        queryset = self.view.filter_future_releases(queryset, future_releases)
        results = list(queryset)

        self.assertEqual(len(results), 3)

    def test_filter_price_range_no_matches(self):
        '''
        Ensure price filter method returns no matches for no match price range
        '''
        price_lower_bound = 0.0
        price_upper_bound = 1.0
        price = [price_lower_bound, price_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_price(queryset, price)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_price_range_all_matches(self):
        '''
        Ensure price filter method returns all database entries for encompassing price range
        '''
        price_lower_bound = 0.0
        price_upper_bound = 100000.0
        price = [price_lower_bound, price_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_price(queryset, price)
        results = list(queryset)

        self.assertEqual(len(results), 3)

    def test_filter_price_range_no_matches_invalid_range(self):
        '''
        Ensure price filter method returns no matches for upper bound before lower bound
        '''
        price_lower_bound = 100.0
        price_upper_bound = 0.0
        price = [price_lower_bound, price_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_price(queryset, price)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_price_lower_bound_all_matches(self):
        '''
        Ensure price filter method returns all database entries for encompassing lower bound (no upper bound)
        '''
        price_lower_bound = 0.0
        price_upper_bound = None
        price = [price_lower_bound, price_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_price(queryset, price)
        results = list(queryset)

        self.assertEqual(len(results), 3)

    def test_filter_price_no_matches_bad_lower_bound(self):
        '''
        Ensure price filter method returns no matches for lower bound higher than all database entries
        '''
        price_lower_bound = 100.0
        price_upper_bound = None
        price = [price_lower_bound, price_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_price(queryset, price)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_price_upper_bound_all_matches(self):
        '''
        Ensure price filter method returns all database entries for encompassing lower bound (no upper bound)
        '''
        price_lower_bound = None
        price_upper_bound = 100000.0
        price = [price_lower_bound, price_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_price(queryset, price)
        results = list(queryset)

        self.assertEqual(len(results), 3)

    def test_filter_price_no_matches_bad_upper_bound(self):
        '''
        Ensure price filter method returns no matches for lower bound higher than all database entries
        '''
        price_lower_bound = None
        price_upper_bound = 0.0
        price = [price_lower_bound, price_upper_bound]
        queryset = self.view.get_queryset()
        queryset = self.view.filter_price(queryset, price)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_search_name_no_matches(self):
        '''
        Ensure search filter method returns no matches for no matching name keywords
        '''
        search = 'Invalid'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_search(queryset, search)
        results = list(queryset)

        self.assertEqual(len(results), 0)

    def test_filter_search_name_non_exact_match(self):
        '''
        Ensure search filter method returns one match for a non exact match
        '''
        search = 'Optemus'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_search(queryset, search)
        results = list(queryset)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Optimus Prime')

    def test_filter_search_name_exact_match(self):
        '''
        Ensure search filter method returns one match for exact match
        '''
        search = 'Optimus'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_search(queryset, search)
        results = list(queryset)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Optimus Prime')

    def test_filter_search_rank_correct(self):
        '''
        Ensure search filter method similarity rank correctly
        '''
        search = 'Optemus Prime'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_search(queryset, search)
        results = list(queryset)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].name, 'Optimus Prime')
        self.assertEqual(results[1].name, 'Skywarp Prime Multiple Words')

    def test_filter_search_rank_toyline(self):
        '''
        Ensure search filter method similarity finds toyline key words
        '''
        search = 'Generations'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_search(queryset, search)
        results = list(queryset)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].name, 'Bumblebee')
        self.assertEqual(results[1].name, 'Skywarp Prime Multiple Words')

    def test_filter_search_rank_toyline(self):
        '''
        Ensure search filter method similarity finds subline key words
        '''
        search = 'Studio Series'
        queryset = self.view.get_queryset()
        queryset = self.view.filter_search(queryset, search)
        results = list(queryset)

        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].name in 'Bumblebee,Skywarp Prime Multiple Words')
        self.assertTrue(results[1].name in 'Bumblebee,Skywarp Prime Multiple Words')