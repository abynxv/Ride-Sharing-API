from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .all_views.rider_views import RiderViewSet
from .all_views.driver_views import DriverRideViewSet

router = DefaultRouter()
router.register(r'rides', RiderViewSet, basename='rides')
router.register(r'driver/rides', DriverRideViewSet, basename='driver-rides')

urlpatterns = [
    path('', include(router.urls)),
]