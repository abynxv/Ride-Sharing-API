from celery import shared_task
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Ride
from .utils import haversine

STEP_KM = 0.05  # Move 50 meters each tick
COMPLETION_THRESHOLD_KM = 0.03  # Consider ride complete within 30 meters

@shared_task
def simulate_ride_movement():
    rides = Ride.objects.filter(status='in_progress').select_related('driver')
    for ride in rides:
        with transaction.atomic():
            r = Ride.objects.select_for_update().get(pk=ride.pk)

            cur_lat = r.current_latitude or r.pickup_latitude
            cur_lng = r.current_longitude or r.pickup_longitude
            dst_lat = r.dropoff_latitude
            dst_lng = r.dropoff_longitude

            distance = haversine(cur_lat, cur_lng, dst_lat, dst_lng)

            if distance <= COMPLETION_THRESHOLD_KM:
                # Mark ride completed
                r.status = 'completed'
                r.current_latitude = dst_lat
                r.current_longitude = dst_lng
                r.completed_at = timezone.now()
                r.save()

                # Optionally mark driver available (if you track that)
                if r.driver:
                    r.driver.is_available = True
                    r.driver.save()
                continue

            fraction = min(STEP_KM / distance, 1.0)
            new_lat = cur_lat + fraction * (dst_lat - cur_lat)
            new_lng = cur_lng + fraction * (dst_lng - cur_lng)

            r.current_latitude = new_lat
            r.current_longitude = new_lng
            r.save()

            if r.driver:
                r.driver.current_latitude = new_lat
                r.driver.current_longitude = new_lng
                r.driver.save()