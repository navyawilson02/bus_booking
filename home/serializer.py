from rest_framework import serializers
from .models import Bus, Points, Route, Seats, Ticket, Working_days

class RouteBusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['to', 'fro']


class BusSerializer(serializers.ModelSerializer):
    route = RouteBusSerializer()
    class Meta:
        model = Bus
        fields = ['id', 'no', 'type', 'capacity','route']


class WorkingDaySerializer(serializers.ModelSerializer):
    bus = BusSerializer()
    available_seats = serializers.SerializerMethodField()

    class Meta:
       model = Working_days
       fields = ['id','day', 'bus', 'available_seats']

class WorkingDaySerializerDetailed(serializers.ModelSerializer):
    bus = BusSerializer()
    available_seats = serializers.SerializerMethodField()

    class Meta:
       model = Working_days
       fields = ['id', 'day', 'bus', 'available_seats', 'bus__route__points']

    def get_available_seats(self, obj):
        return obj.bus.capacity - obj.seat.all().count()

class SeatsSerializer(serializers.ModelSerializer):
    details = WorkingDaySerializer(source='day')
    class Meta:
       model = Seats
       fields = ['no', 'details']

class PointSerializer(serializers.ModelSerializer):
    class Meta:
       model = Points 
       fields = ['time', 'place']

class PointSerializerDetailed(serializers.ModelSerializer):
    class Meta:
       model = Points 
       fields = ['order', 'time', 'place']

class TicketSerializer(serializers.ModelSerializer):
    seat = SeatsSerializer()
    to = PointSerializer()
    fro = PointSerializer()

    class Meta:
        model = Ticket
        fields = ['seat', 'to', 'fro']
