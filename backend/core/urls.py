from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PackageViewSet, StorageLocationViewSet

router = DefaultRouter()
router.register(r'packages', PackageViewSet)
router.register(r'storage-locations', StorageLocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]