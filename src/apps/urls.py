from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.views.apps_view import AppsViewSet
from apps.views.purchases_view import PurchasesViewSet

router = DefaultRouter()
router.register('apps', AppsViewSet, basename='apps')
router.register('purchases', PurchasesViewSet, basename='purchases')

urlpatterns = [
    path('', include(router.urls))
]
