from django.db.models.query import QuerySet


class FullCleanOnSaveMixin:
    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class OrderMixin:
    def get_queryset(self) -> QuerySet:
        return self.queryset.order_by('id')
