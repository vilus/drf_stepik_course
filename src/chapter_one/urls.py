from django.urls import path

from . import views

urlpatterns = [
    path('recipients/', views.recipients),
    path('recipients/<pk>/', views.recipient),
    path('product-sets/', views.product_sets),
    path('product-sets/<pk>/', views.product_set),
]
