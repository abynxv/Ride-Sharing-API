from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .. models import Ride
from .. serializers import RideSerializer


class DriverRideViewSet(ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ride.objects.filter(status='requested', driver__isnull=True)

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
        ride = get_object_or_404(Ride, pk=pk, driver=request.user)
        new_status = request.data.get('status')
        if new_status not in dict(Ride.STATUS_CHOICES).keys():
            return Response({"error": "Invalid status"}, status=400)
        ride.status = new_status
        ride.save()
        return Response({"message": f"Ride status updated to {new_status}"}, status=status.HTTP_200_OK)
