from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.contrib.postgres.search import TrigramWordSimilarity
from django.utils import timezone
from operator import itemgetter
from datetime import datetime
import numpy as np
import time

from .models import Transformer
from .serializers import TransformerSerializer, TransformerDetailSerializer
from .paginators import TransformerPaginator

class TransformerListView(ListAPIView):
    queryset = Transformer.objects.all().filter(is_visible=True)
    serializer_class = TransformerSerializer


class TransformerDetailView(RetrieveAPIView):
    queryset = Transformer.objects.all().filter(is_visible=True)
    serializer_class = TransformerDetailSerializer


class TransfomerSearchView(APIView):
    queryset = Transformer.objects.all().filter(is_visible=True)
    serializer_class = TransformerSerializer
    paginator = TransformerPaginator()
    filter_fields = ['toyline', 'subline', 'size_class', 'release_date', 'price', 'manufacturer']

    def get_queryset(self):
        return Transformer.objects.all().filter(is_visible=True)

    def filter_toyline(self, queryset, toyline_filter):
        if toyline_filter:
            print(toyline_filter)
            return queryset.exclude(toyline__name__in=toyline_filter)
        return queryset

    def filter_subline(self, queryset, subline_filter):
        if subline_filter:
            return queryset.exclude(subline__name__in=subline_filter)
        return queryset

    def filter_size_class(self, queryset, size_class_filter):
        if size_class_filter:
            return queryset.exclude(size_class__in=size_class_filter)
        return queryset

    def filter_manufacturer(self, queryset, manufacturer_filter):
        if manufacturer_filter:
            return queryset.exclude(manufacturer__in=manufacturer_filter)
        return queryset

    def filter_release_date(self, queryset, release_date_bounds):
        '''
        Release date filter format: 
            YYYY-MM-DD,YYYY-MM-DD
            Lower Bound,Upper Bound
        '''
        lower_bound = release_date_bounds['lower']
        upper_bound = release_date_bounds['upper']

        # Filter by lower bound
        if lower_bound:
            lower_bound = datetime.strptime(lower_bound, '%Y-%m-%d').date()
            queryset = queryset.filter(release_date__gte=lower_bound)
        
        # Filter by upper bound
        if upper_bound:
            upper_bound = datetime.strptime(upper_bound, '%Y-%m-%d').date()
            queryset = queryset.filter(release_date__lte=upper_bound)
        return queryset

    def filter_future_releases(self, queryset, future_release_filter):
        if not future_release_filter:
            queryset = queryset.filter(release_date__lte=timezone.now().date())
        return queryset

    def filter_price(self, queryset, price_filter):
        '''
        Price filter format: 
            x.xx,y.yy
            Lower Bound,Upper Bound
        '''
        upper_bound = price_filter['upper']
        lower_bound = price_filter['lower']

        # Filter by lower bound
        if lower_bound:
            queryset = queryset.filter(price__gte=lower_bound)
        
        # Filter by upper bound
        if upper_bound:
            queryset = queryset.filter(price__lte=upper_bound)
        return queryset

    def filter_search(self, queryset, search_keywords):
        if not search_keywords:
            return queryset

        search_fields = ['name', 'toyline', 'subline', 'size_class']
        similarities = [TrigramWordSimilarity(search_keywords, field) for field in search_fields]
        similarity = sum(similarities) / len(similarities)
        return queryset.annotate(similarity=similarity).filter(similarity__gt=0.1).order_by('-similarity')

    def get_available_filters(self, queryset):
        # Get all available filter field values
        filter_field_values = queryset.values_list(*self.filter_fields)
        
        if not filter_field_values:
            return {
                'toyline': [],
                'subline': [],
                'size_class': [],
                'manufacturer': [],
                'release_date': {
                    'min': 0,
                    'max': 0
                },
                'price': {
                    'upper': 0,
                    'lower': 0
                }
            }
        
        value_np_array = np.core.records.fromrecords(filter_field_values, names=self.filter_fields)

        # Sort filter fields by frequency - https://stackoverflow.com/a/66064470
        sorted_filter_options = {}
        for name in self.filter_fields:
            col = value_np_array[name]
            if name in ['release_date', 'price']:
                sorted_filter_options[name] = {
                    'min': col.min(), 
                    'max': col.max()
                }
                continue
            unique_values, frequency = np.unique(col, return_counts=True)
            options = list((val, freq) for val,freq in zip(unique_values.tolist(), frequency))        
            sorted_filter_options[name] = sorted(options, key=itemgetter(1), reverse=True)
        return sorted_filter_options

    def post(self, request, format=None):
        start_time = time.time()

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

        # Filter for search keywords by trigram similarity
        search_keywords = data['search']
        queryset = self.filter_search(queryset, search_keywords)

        # Order by specified column
        order_by = data['order']
        ascending = data['ascending']

        # Assign order direction
        if ascending.lower() == 'false':
            order_by = '-' + order_by

        # Default order by name
        if order_by == '' or order_by == '-':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by(order_by)

        # Paginate queryset
        page_results = self.paginator.paginate_queryset(queryset=queryset, request=request)
        
        # Serialize results
        serializer = TransformerSerializer(page_results, many=True)

        # Paginate response
        response = self.paginator.get_paginated_response(serializer.data)

        # Add available filter options to response
        available_filters = self.get_available_filters(queryset) 
        response.data['available_filters'] = available_filters

        # Add response time to response
        response.data['response_time'] = round(time.time() - start_time, 2)

        return response

