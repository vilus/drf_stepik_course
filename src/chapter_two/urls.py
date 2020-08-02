from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('products_set', views.ProductSetViewSet)
router.register('recipients', views.RecipientViewSet)
router.register('orders', views.OrderViewSet)

urlpatterns = router.urls
