import pathlib

from django.apps import apps

app_name = pathlib.Path(__file__).resolve().parent.parent.parent.name
ProductSet = apps.get_model(app_name, 'ProductSet')
Recipient = apps.get_model(app_name, 'Recipient')
Order = apps.get_model(app_name, 'Order')
