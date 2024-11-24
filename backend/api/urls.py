# backend/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PackageViewSet, StorageLocationViewSet, ScheduledEventViewSet

router = DefaultRouter()
router.register(r'packages', PackageViewSet)
router.register(r'storage-locations', StorageLocationViewSet)
router.register(r'scheduled-events', ScheduledEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]