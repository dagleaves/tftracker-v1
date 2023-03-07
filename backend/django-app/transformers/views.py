from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import Count, Max, Min
from django.utils import timezone
from datetime import datetime
import time

from rest_framework.response import Response
from rest_framework import status

from .models import Transformer
from .serializers import TransformerSerializer, TransformerDetailSerializer
from .paginators import TransformerPaginator

class TransformerListView(ListAPIView):
    queryset = Transformer.objects.all().filter(is_visible=True)
    serializer_class = TransformerSerializer


class TransformerDetailView(RetrieveAPIView):
    queryset = Transformer.objects.all().filter(is_visible=True)
    serializer_class = TransformerDetailSerializer


class TransformerAvailableFiltersView(APIView):
    filter_fields = ['toyline', 'subline', 'size_class', 'manufacturer']
    min_max_fields = ['release_date', 'price']
    manufacturer_choices = dict(Transformer.MANUFACTURERS)

    def get_queryset(self):
        return Transformer.objects.all().filter(is_visible=True)

    def get(self, request, format=None):
        available_filters = {}
        for field in self.filter_fields:
            available = list(self.get_queryset().order_by().values_list(field).annotate(count=Count(field)).distinct().order_by('-count').values_list(field, flat=True))
            if field == 'manufacturer':
                available = [self.manufacturer_choices[choice] for choice in available]
            available_filters[field] = available

        for field in self.min_max_fields:
            min_value = list(self.get_queryset().aggregate(Min(field)).values())[0]
            max_value = list(self.get_queryset().aggregate(Max(field)).values())[0]
            available_filters[field] = (min_value, max_value)

        return Response(available_filters, status=status.HTTP_200_OK)

class TransfomerSearchView(APIView):
    queryset = Transformer.objects.all().filter(is_visible=True)
    serializer_class = TransformerSerializer
    paginator = TransformerPaginator()

    search_fields = ['name', 'toyline', 'subline', 'size_class']
    filter_fields = ['toyline', 'subline', 'size_class', 'manufacturer']
    min_max_fields = ['release_date', 'price']
    manufacturer_choices = dict(Transformer.MANUFACTURERS)

    def get_queryset(self):
        return Transformer.objects.all().filter(is_visible=True)

    def filter_toyline(self, queryset, toyline_filter):
        if toyline_filter:
            return queryset.filter(toyline__name__in=toyline_filter)
        return queryset

    def filter_subline(self, queryset, subline_filter):
        if subline_filter:
            return queryset.filter(subline__name__in=subline_filter)
        return queryset

    def filter_size_class(self, queryset, size_class_filter):
        if size_class_filter:
            return queryset.filter(size_class__in=size_class_filter)
        return queryset

    def filter_manufacturer(self, queryset, manufacturer_filter):
        manufacturer_filter = [manufacturer[0] for manufacturer in manufacturer_filter]
        if manufacturer_filter:
            return queryset.filter(manufacturer__in=manufacturer_filter)
        return queryset

    def filter_release_date(self, queryset, release_date_bounds):
        '''
        Release date filter format: 
            YYYY-MM-DD,YYYY-MM-DD
            Lower Bound,Upper Bound
        '''
        lower_bound = release_date_bounds[0]
        upper_bound = release_date_bounds[1]

        # Filter by lower bound
        if lower_bound is not None:
            lower_bound = datetime.strptime(lower_bound, '%Y-%m-%d').date()
            queryset = queryset.filter(release_date__gte=lower_bound)
        
        # Filter by upper bound
        if upper_bound is not None:
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
        if not price_filter:
            return queryset

        lower_bound = price_filter[0]
        upper_bound = price_filter[1]

        # Filter by lower bound
        if lower_bound is not None:
            queryset = queryset.filter(price__gte=lower_bound)
        
        # Filter by upper bound
        if upper_bound is not None:
            queryset = queryset.filter(price__lte=upper_bound)
        return queryset

    def filter_search(self, queryset, search_keywords):
        if not search_keywords:
            return queryset

        similarities = [TrigramWordSimilarity(search_keywords, field) for field in self.search_fields]
        similarity = sum(similarities) / len(similarities)
        return queryset.annotate(similarity=similarity).filter(similarity__gt=0.1).order_by('-similarity')

    def get_available_filters(self, queryset):
        available_filters = {}
        for field in self.filter_fields:
            available = list(queryset.order_by().values_list(field).annotate(count=Count(field)).distinct().order_by('-count'))
            if field == 'manufacturer':
                available = [(self.manufacturer_choices[choice], freq) for choice, freq in available]
            available_filters[field] = available

        for field in self.min_max_fields:
            min_value = list(queryset.aggregate(Min(field)).values())[0]
            max_value = list(queryset.aggregate(Max(field)).values())[0]
            available_filters[field] = (min_value, max_value)

        return available_filters


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

        # Add response time to response
        response.data['response_time'] = round(time.time() - start_time, 2)

        # Add available filters to response
        available_filters = self.get_available_filters(queryset)
        response.data['available_filters'] = available_filters

        return response

