from rest_framework import serializers
from . models import Ride


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        if data['pickup_location'] == data['dropoff_location']:
            raise serializers.ValidationError("Pickup and dropoff locations cannot be the same.")
        return data

