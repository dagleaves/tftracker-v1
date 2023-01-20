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

    class Meta:
        model = Transformer
        fields = ['id', 'name', 'release_date', 'price', 'toyline', 'subline', 'size_class', 'manufacturer']


class TransformerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transformer
        fields = '__all__'