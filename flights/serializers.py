from rest_framework import serializers
from .models import Flight, Booking

class FlightSerializer(serializers.ModelSerializer):
    origin = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()

    class Meta:
        model = Flight
        fields = ['id', 'origin', 'destination', 'duration', 'capacity']


class BookingSerializer(serializers.Serializer):
    flight_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
