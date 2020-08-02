import datetime
import random
import uuid

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from . import _app_models as models


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        if not settings.DEBUG:
            self.stdout.write(self.style.WARNING('Only when settings.DEBUG is True'))
            return

        for i in range(42):
            models.ProductSet.objects.create(title=f'title_{i}',
                                             description=f'description_{i}')

            models.Recipient.objects.create(surname=f'surname_{i}',
                                            name=f'name_{i}',
                                            patronymic=f'patronymic_{i}',
                                            phone_number=f'phone_number_{i}')

        products = list(models.ProductSet.objects.all())
        recipients = list(models.Recipient.objects.all())
        now = timezone.now()

        for _ in range(42):
            recipient = random.choice(recipients)
            for _ in range(random.randrange(0, 4)):
                deliver_at = now + datetime.timedelta(minutes=random.randrange(30, 360))
                models.Order.objects.create(
                    product_set=random.choice(products),
                    recipient=recipient,
                    delivery_address=f'{uuid.uuid4()}',
                    deliver_at=deliver_at,
                    status=random.choice(models.Order.Status.choices)[0]
                )

        self.stdout.write(self.style.SUCCESS('OK'))
