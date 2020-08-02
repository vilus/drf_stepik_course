from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    SerializerMethodField,
)

from . import models


class AppBaseMeta:
    fields = '__all__'


class ProductSetSerializer(HyperlinkedModelSerializer):
    class Meta(AppBaseMeta):
        model = models.ProductSet


class NestedProductSetSerializer(ModelSerializer):
    class Meta:
        model = models.ProductSet
        fields = ['title']


class RecipientSerializer(HyperlinkedModelSerializer):
    class Meta(AppBaseMeta):
        model = models.Recipient


class NestedRecipientSerializer(ModelSerializer):
    class Meta:
        model = models.Recipient
        fields = ['name', 'patronymic', 'phone_number']


class OrderSerializer(HyperlinkedModelSerializer):
    product_set_detail = SerializerMethodField()
    recipient_detail = SerializerMethodField()

    class Meta(AppBaseMeta):
        model = models.Order

    @staticmethod
    def get_product_set_detail(obj: models.Order) -> dict:
        return NestedProductSetSerializer(obj.product_set).data

    @staticmethod
    def get_recipient_detail(obj: models.Order) -> dict:
        return NestedRecipientSerializer(obj.recipient).data
