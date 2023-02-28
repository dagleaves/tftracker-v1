from rest_framework import serializers

from .models import Collection, CollectionItem


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = '__all__'


class CollectionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'name', 'public']


class CollectionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionItem
        fields = '__all__'