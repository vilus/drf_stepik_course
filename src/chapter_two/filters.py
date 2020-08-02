from django_filters.rest_framework import FilterSet
from django_filters import DateTimeFilter

from . import models


class OrderFilter(FilterSet):
    created_at = DateTimeFilter(field_name='created_at')

    class Meta:
        model = models.Order
        fields = {
            'created_at': ['gte', 'lte', 'date'],
            'status': ['exact'],
            'product_set__title': ['exact'],
        }


class ProductSetFilter(FilterSet):
    class Meta:
        model = models.ProductSet
        fields = {
            'title': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
        }
