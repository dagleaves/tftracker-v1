from rest_framework import serializers

from .models import Collection, CollectionItem
from transformers.serializers import TransformerCollectionSerializer

class CollectionItemSerializer(serializers.ModelSerializer):
    transformer = TransformerCollectionSerializer()

    class Meta:
        model = CollectionItem
        fields = ['id', 'priority', 'date', 'transformer']


class CollectionSerializer(serializers.ModelSerializer):
    items = CollectionItemSerializer(many=True)
    length = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = '__all__'

    def get_length(self, obj):
        return obj.items.all().count()


class CollectionListSerializer(serializers.ModelSerializer):
    length = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ['id', 'name', 'public', 'length']
    
    def get_length(self, obj):
        return obj.items.all().count()
