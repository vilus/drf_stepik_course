from rest_framework import mixins, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from . import (
    serializers,
    models,
    paginations,
    mixins as app_mixins,
    filters as app_filters,
)


class ProductSetViewSet(app_mixins.OrderMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.ProductSet.objects.all()
    serializer_class = serializers.ProductSetSerializer
    pagination_class = paginations.DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = app_filters.ProductSetFilter


class RecipientViewSet(app_mixins.OrderMixin, viewsets.ModelViewSet):
    queryset = models.Recipient.objects.all()
    serializer_class = serializers.RecipientSerializer
    pagination_class = paginations.DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class OrderViewSet(app_mixins.OrderMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = (
        models.Order.objects.all()
        .select_related('product_set', 'recipient')
        .defer('product_set__description')
    )
    serializer_class = serializers.OrderSerializer
    pagination_class = paginations.DefaultPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = app_filters.OrderFilter
    ordering_fields = ['created_at', 'deliver_at']
