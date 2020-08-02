from django.core.management.base import BaseCommand
from django.conf import settings

from . import _app_models as models


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        if not settings.DEBUG:
            self.stdout.write(self.style.WARNING('Only when settings.DEBUG is True'))
            return

        models.ProductSet.objects.all().delete()
        models.Recipient.objects.all().delete()
        models.Order.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('OK'))
