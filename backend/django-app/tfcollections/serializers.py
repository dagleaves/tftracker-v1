from rest_framework import serializers

from .models import Collection, CollectionItem


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = '__all__'


class CollectionListSerializer(serializers.ModelSerializer):
    length = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ['id', 'name', 'public', 'length']
    
    def get_length(self, obj):
        return obj.items.all().count()


class CollectionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionItem
        fields = '__all__'