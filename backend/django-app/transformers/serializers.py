from rest_framework import serializers

from .models import Transformer, Toyline, Subline


class SublineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subline
        fields = ['name', 'toyline']


class ToylineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Toyline
        fields = ['name']


class TransformerSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(source='get_manufacturer_display')

    class Meta:
        model = Transformer
        fields = ['id', 'name', 'release_date', 'price', 'toyline', 'subline', 'size_class', 'manufacturer']


class TransformerCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transformer
        fields = ['id', 'name', 'toyline', 'subline', 'size_class']


class TransformerDetailSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(source='get_manufacturer_display')

    class Meta:
        model = Transformer
        fields = '__all__'