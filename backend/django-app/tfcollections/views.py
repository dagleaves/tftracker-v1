from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response

from .models import Collection
from .serializers import CollectionSerializer, CollectionListSerializer


class MyCollectionsView(ListAPIView):
    serializer_class = CollectionListSerializer
    queryset = Collection.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class MyCollectionView(RetrieveUpdateDestroyAPIView):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)