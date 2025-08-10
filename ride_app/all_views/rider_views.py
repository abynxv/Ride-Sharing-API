from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .. models import Ride
from .. serializers import RideSerializer
from .. permissions import IsRider


class RiderViewSet(ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated, IsRider]

    def perform_create(self, serializer):
        user = self.request.user
        if user.ride_block_until and timezone.now() < user.ride_block_until:
            raise ValidationError({"error": "You cannot request a new ride yet."})
        serializer.save(rider=user)

    def get_queryset(self):
        user = self.request.user
        return Ride.objects.filter(rider=user)

    def update(self, request, *args, **kwargs):
        ride = self.get_object()
        if ride.status != 'requested':
            return Response({"error": "Unable to edit ride once it is accepted or later."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='cancel-ride')
    def cancel_ride(self, request, pk=None):
        ride = get_object_or_404(Ride, pk=pk, rider=request.user)

        if ride.status not in ['requested', 'accepted']:
            return Response({"error": "Cannot cancel this ride."}, status=status.HTTP_400_BAD_REQUEST)

        if ride.status == 'accepted':
            request.user.ride_block_until = timezone.now() + timedelta(minutes=10)
            request.user.save()

        ride.status = 'cancelled'
        ride.save()
        return Response({"message": "Ride cancelled successfully."})

    @action(detail=True, methods=['get'], url_path='track-ride')
    def track_ride(self, request, pk=None):
        ride = get_object_or_404(Ride, pk=pk, rider=request.user)

        if not ride.driver:
            return Response({"error": "Driver has not been assigned yet."}, status=status.HTTP_400_BAD_REQUEST)

        driver = ride.driver
        return Response({
            "ride_status": ride.status,
            "driver_location": {
                "latitude": driver.current_latitude,
                "longitude": driver.current_longitude
            }
        }, status=status.HTTP_200_OK)