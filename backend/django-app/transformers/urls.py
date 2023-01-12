from django.urls import path

from .views import TransformerListView, TransformerDetailView, TransfomerSearchView

urlpatterns = [
    path('', TransformerListView.as_view(), name='list-view'),
    path('search', TransfomerSearchView.as_view(), name='search-view'),
    path('<pk>', TransformerDetailView.as_view(), name='detail-view'),
]