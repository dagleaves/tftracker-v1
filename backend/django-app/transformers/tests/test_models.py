from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from transformers.models import Transformer, Toyline, Subline

import os
import shutil

class TransformerModelTests(TestCase):

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
        return Transformer.objects.create(picture=picture, name=name, release_date=release_date, price=price, toyline=toyline, subline=subline, size_class=size_class, description=description, manufacturer=manufacturer)

    def setUp(self):
        def_toyline, _ = Toyline.objects.get_or_create(name='None')
        def_subline, _ = Subline.objects.get_or_create(name='None', defaults={'toyline': def_toyline})
        self.generations, _ = Toyline.objects.get_or_create(name='Generations')
        self.studio_series, _ = Subline.objects.get_or_create(name='Studio Series', defaults={'toyline':  self.generations})
        legacy, _ = Subline.objects.get_or_create(name='Legacy', defaults={'toyline':  self.generations})
        earthspark, _ = Toyline.objects.get_or_create(name='EarthSpark')
        self.create_default_transformer(toyline=self.generations, subline=self.studio_series)

    def tearDown(self):
        shutil.rmtree('media', ignore_errors=True)
        os.mkdir('media')

    def test_setup(self):
        pass

    def test_sanity(self):
        '''
        Ensure model fields behave as expected
        '''
        self.assertEqual(Transformer.objects.count(), 1)

        tf = Transformer.objects.get(name='Bumblebee')
        self.assertIsNotNone(tf)
        self.assertEqual(tf.name, 'Bumblebee')
        self.assertEqual(tf.picture.name, 'transformers/foo.gif')
        self.assertEqual(tf.release_date, timezone.now().date())
        self.assertEqual(tf.price, 19.99)
        self.assertEqual(tf.toyline.name, 'Generations')
        self.assertEqual(tf.subline.name, 'Studio Series')
        self.assertEqual(tf.size_class, 'Deluxe')
        self.assertEqual(tf.description, '')
        self.assertEqual(tf.manufacturer, 'H')
        self.assertEqual(str(tf), 'Bumblebee')
        self.assertTrue(tf.is_visible)

    def test_duplicate_names(self):
        '''
        Ensure auto slug does not create identical slugs for the same name
        '''
        tf1 = self.create_default_transformer(name='Optimus Prime', toyline=self.generations, subline=self.studio_series)
        tf2 = self.create_default_transformer(name='Optimus Prime', toyline=self.generations, subline=self.studio_series, price=100.00)
        self.assertIsNotNone(tf1)
        self.assertIsNotNone(tf2)