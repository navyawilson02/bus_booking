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
    class Meta:
       model = Working_days
       fields = ['day', 'bus'] 

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
