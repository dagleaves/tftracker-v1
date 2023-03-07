from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from .models import Collection
from .serializers import CollectionSerializer, CollectionListSerializer


class MyCollectionsView(ListAPIView):
    serializer_class = CollectionListSerializer
    queryset = Collection.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user).order_by('name')


class MyCollectionView(RetrieveUpdateDestroyAPIView):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class PublicCollectionsView(ListAPIView):
    serializer_class = CollectionListSerializer
    queryset = Collection.objects.all()

    def get_queryset(self):
        user_pk = self.kwargs.get('pk')
        return self.queryset.filter(user=user_pk, public=True).order_by('name')


class PublicCollectionView(RetrieveAPIView):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    def get_queryset(self):
        return self.queryset.filter(public=True)