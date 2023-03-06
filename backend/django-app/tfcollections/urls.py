from django.urls import path

from .views import MyCollectionsView, MyCollectionView, PublicCollectionsView, PublicCollectionView

urlpatterns = [
    path('me/', MyCollectionsView.as_view(), name='my-collections-list'),
    path('me/<int:pk>/', MyCollectionView.as_view(), name='my-collection'),
    path('user/<int:pk>/', PublicCollectionsView.as_view(), name='public-collections-list'),
    path('public/<int:pk>/', PublicCollectionView.as_view(), name='public-collection'),
]