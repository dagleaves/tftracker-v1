from datetime import datetime
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.postgres.search import TrigramWordSimilarity
from django.utils import timezone
from django.db.models import Avg

from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Transformer
from .serializers import TransformerSerializer, TransformerListSerializer, TransformerDetailSerializer

class TransformerListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Transformer.objects.all().filter(is_visible=True)
    serializer_class = TransformerListSerializer


class TransformerDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Transformer.objects.all().filter(is_visible=True)
    serializer_class = TransformerSerializer


class TransfomerSearchView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Transformer.objects.all().filter(is_visible=True)
    serializer_class = TransformerDetailSerializer

    def get_queryset(self):
        return Transformer.objects.all().filter(is_visible=True)

    def filter_toyline(self, queryset, toyline_filter):
        if toyline_filter == '':
            return queryset

        if ',' in toyline_filter:
            toylines = toyline_filter.split(',')
        else:
            toylines = [toyline_filter,]
        return queryset.filter(toyline__name__in=toylines)

    def filter_subline(self, queryset, subline_filter):
        if subline_filter == '':
            return queryset

        if ',' in subline_filter:
            sublines = subline_filter.split(',')
        else:
            sublines = [subline_filter,]
        return queryset.filter(subline__name__in=sublines)

    def filter_size_class(self, queryset, size_class_filter):
        if size_class_filter == '':
            return queryset

        if ',' in size_class_filter:
            size_classes = size_class_filter.split(',')
        else:
            size_classes = [size_class_filter,]
        
        # Replace None string with None variable
        if 'None' in size_classes:
            size_classes[size_classes.index('None')] = None
        return queryset.filter(size_class__in=size_classes)

    def filter_manufacturer(self, queryset, manufacturer_filter):
        if manufacturer_filter == '':
            return queryset

        if ',' in manufacturer_filter:
            manufacturers = manufacturer_filter.split(',')
        else:
            manufacturers = [manufacturer_filter,]
        return queryset.filter(manufacturer__in=manufacturers)

    def filter_release_date(self, queryset, release_date_bounds):
        '''
        Release date filter format: 
            YYYY-MM-DD,YYYY-MM-DD
            Lower Bound,Upper Bound
        '''
        if release_date_bounds == '':
            return queryset
            
        lower_bound, upper_bound = release_date_bounds.split(',')
        # Filter by lower bound
        if lower_bound != '':
            lower_bound = datetime.strptime(lower_bound, '%Y-%m-%d').date()
            queryset = queryset.filter(release_date__gte=lower_bound)
        
        # Filter by upper bound
        if upper_bound != '':
            upper_bound = datetime.strptime(upper_bound, '%Y-%m-%d').date()
            queryset = queryset.filter(release_date__lte=upper_bound)
        return queryset

    def filter_future_releases(self, queryset, future_release_filter):
        if future_release_filter == 'false':
            queryset = queryset.filter(release_date__lte=timezone.now().date())
        return queryset

    def filter_price(self, queryset, price_filter):
        '''
        Price filter format: 
            x.xx,y.yy
            Lower Bound,Upper Bound
        '''
        if price_filter == '':
            return queryset
        lower_bound, upper_bound = price_filter.split(',')
        
        # Filter by lower bound
        if lower_bound != '':
            queryset = queryset.filter(price__gte=lower_bound)
        
        # Filter by upper bound
        if upper_bound != '':
            queryset = queryset.filter(price__lte=upper_bound)
        return queryset

    def filter_search(self, queryset, search_keywords):
        if search_keywords == '':
            return queryset

        search_fields = ['name', 'toyline', 'subline', 'size_class']
        similarities = [TrigramWordSimilarity(search_keywords, field) for field in search_fields]
        similarity = sum(similarities) / len(similarities)
        return queryset.annotate(similarity=similarity).filter(similarity__gt=0.1).order_by('-similarity')

    def post(self, request, format=None):
        data = request.data
        queryset = self.get_queryset()

        # Filter for toyline
        toyline_filter = data['toyline']
        queryset = self.filter_toyline(queryset, toyline_filter)

        # Filter for subline
        subline_filter = data['subline']
        queryset = self.filter_subline(queryset, subline_filter)

        # Filter for size class
        size_class_filter = data['size_class']
        queryset = self.filter_size_class(queryset, size_class_filter)

        # Filter for manufacturer
        manufacturer_filter = data['manufacturer']
        queryset = self.filter_manufacturer(queryset, manufacturer_filter)
        
        # Filter for release date
        release_date_bounds = data['release_date']
        queryset = self.filter_release_date(queryset, release_date_bounds)

        # Filter for only upcoming releases
        future_release_filter = data['future_releases']
        queryset = self.filter_future_releases(queryset, future_release_filter)

        # Filter for price
        price_filter = data['price']
        queryset = self.filter_price(queryset, price_filter)

        # TODO: consider using Trigram similarity
        search_keywords = data['search']
        queryset = self.filter_search(queryset, search_keywords)
        
        serializer = TransformerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


