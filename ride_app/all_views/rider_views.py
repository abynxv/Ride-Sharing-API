from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .. models import Ride
from .. serializers import RideSerializer


class RiderViewSet(ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)

    def get_queryset(self):
        return Ride.objects.filter(rider=self.request.user)

    def update(self, request, *args, **kwargs):
        ride = self.get_object()
        if ride.status != 'requested':
            return Response({"error": "Unable to edit ride"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='cancel-ride')
    def cancel_ride(self, request, pk=None):
        ride = get_object_or_404(Ride, pk=pk, rider=request.user)
        if ride.status == 'cancelled':
            return Response({"error": "Ride already cancelled."}, status=status.HTTP_400_BAD_REQUEST)
        ride.status = 'cancelled'
        ride.save()
        return Response({"message": "Ride cancelled successfully."}, status=status.HTTP_200_OK)