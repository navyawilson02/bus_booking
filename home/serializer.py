from rest_framework import serializers
from .models import Bus, Points, Route, Stops, Ticket, Working_days, Traveller


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Points
        fields = ['time', 'place', 'order', 'id']


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stops
        fields = ['id', 'place']


class RouteBusSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['name', 'points']


class BusSerializer(serializers.ModelSerializer):
    route = RouteBusSerializer()

    class Meta:
        model = Bus
        fields = ['id', 'no', 'type', 'capacity', 'route']


class WorkingDaySerializer(serializers.ModelSerializer):
    bus = BusSerializer()
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Working_days
        fields = ['id', 'day', 'bus', 'available_seats']

    def get_available_seats(self, obj):
        return obj.bus.capacity - obj.seat.all().count()


class WorkingDayDetailedSerializer(serializers.ModelSerializer):
    bus = BusSerializer()
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Working_days
        fields = ['id', 'day', 'bus', 'available_seats']

    def get_available_seats(self, obj):
        seats = []
        for i in range(1, obj.bus.capacity + 1):
            seats.append({"no": i, "booked": Ticket.objects.filter(day=obj, no=i).exists()})
        return seats


class StopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stops
        fields = ['place', 'id']


class PointSerializerDetailed(serializers.ModelSerializer):
    place = StopsSerializer()

    class Meta:
        model = Points
        fields = ['order', 'time', 'place']


class TravellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traveller
        fields = ['name', 'age', 'gender']


class TicketSerializer(serializers.ModelSerializer):
    details = WorkingDaySerializer(source='day')
    traveller = TravellerSerializer()
    to = PointSerializerDetailed()
    fro = PointSerializerDetailed()

    class Meta:
        model = Ticket
        fields = ['id', 'no', 'details', 'to', 'fro', 'traveller']
