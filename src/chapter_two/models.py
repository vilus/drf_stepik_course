from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    DateTimeField,
    Model,
    ForeignKey,
    TextChoices,
    TextField,
    SET_NULL,
)

from . import mixins


class ProductSet(Model):
    title = CharField(max_length=512)
    description = TextField()

    def __str__(self) -> str:
        return f'{self.title}'


class Recipient(Model):
    surname = CharField(max_length=64)
    name = CharField(max_length=64)
    patronymic = CharField(max_length=64, null=True)
    phone_number = CharField(max_length=32)

    def __str__(self) -> str:
        return f'{self.name} {self.surname}: {self.phone_number}'


class Order(mixins.FullCleanOnSaveMixin, Model):
    class Status(TextChoices):
        CREATED = 'created'
        DELIVERED = 'delivered'
        PROCESSED = 'processed'
        CANCELLED = 'cancelled'

    status = CharField(max_length=16, choices=Status.choices, default=Status.CREATED)
    created_at = DateTimeField(default=timezone.now)
    product_set = ForeignKey(ProductSet, null=True, on_delete=SET_NULL)

    recipient = ForeignKey(Recipient, null=True, on_delete=SET_NULL)
    deliver_at = DateTimeField()
    delivery_address = CharField(max_length=512)

    def clean(self) -> None:
        # FIXME: extract to more appropriate place!
        super().clean()

        if self.deliver_at < self.created_at:
            raise ValidationError(
                {'deliver_at': 'Delivery date cannot be earlier than order creation date'}
            )
