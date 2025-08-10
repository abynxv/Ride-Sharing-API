from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .. models import Ride
from .. serializers import RideSerializer
from .. permissions import IsDriver
from .. utils import haversine


class DriverRideViewSet(ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated, IsDriver]

    def get_queryset(self):
        driver_lat = self.request.user.current_latitude
        driver_lon = self.request.user.current_longitude
        radius_km = 5
        rides = Ride.objects.filter(status='requested', driver__isnull=True)
        nearby_rides = []
        
        for ride in rides:
            dist = haversine(driver_lat, driver_lon, ride.pickup_latitude, ride.pickup_longitude)
            if dist <= radius_km:
                nearby_rides.append(ride.id)

        return Ride.objects.filter(id__in=nearby_rides)

    @action(detail=True, methods=['post'], url_path='accept-ride')
    def accept_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.driver:
            return Response({"error": "Ride already accepted by another driver."}, status=status.HTTP_400_BAD_REQUEST)
        ride.driver = request.user
        ride.status = 'accepted'
        ride.save()
        return Response({"message": "Ride accepted successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='update_status')
    def update_status(self, request, pk=None):
        ride = self.get_object_or_404(Ride, pk=pk, driver=request.user)
        new_status = request.data.get('status')

        if new_status not in dict(Ride.STATUS_CHOICES).keys():
            return Response({"error": "Invalid status"}, status=400)

        if new_status == 'in_progress':
            if ride.current_latitude is None or ride.current_longitude is None:
                ride.current_latitude = ride.pickup_latitude
                ride.current_longitude = ride.pickup_longitude

        ride.status = new_status
        ride.save()
        return Response({"message": f"Ride status updated to {new_status}"})
    
    @action(detail=False, methods=['post'], url_path='update-location')
    def update_location(self, request): 
        user = request.user
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        
        if latitude is None or longitude is None:
            return Response({"error": "Latitude and longitude are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.current_latitude = latitude
        user.current_longitude = longitude
        user.save()    
        return Response({"message": "Location updated successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='assigned-rides')
    def assigned_rides(self, request):
        rides = Ride.objects.filter(driver=request.user)
        serializer = self.get_serializer(rides, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='assigned-ride-detail')
    def assigned_ride_detail(self, request, pk=None):
        ride = get_object_or_404(Ride, pk=pk, driver=request.user)
        serializer = self.get_serializer(ride)
        return Response(serializer.data)
