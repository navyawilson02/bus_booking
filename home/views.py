from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, filters
import django_filters
from django.core import serializers
from django.shortcuts import redirect
from .models import *
from .serializer import BusSerializer, PointSerializer, StopSerializer, TicketSerializer, WorkingDayDetailedSerializer, \
    WorkingDaySerializer
from rest_framework.decorators import action, parser_classes
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser


# Create your views here.

# @login_required(login_url="/login")
def HomePage(request):
    print("HOMEEE")
    context = {}
    stops = [StopSerializer(stop).data for stop in Stops.objects.all()]
    context["places"] = stops
    return render(request, template_name="home.html", context=context)


def ContactPage(request):
    return render(request, template_name="contact.html")


def AboutPage(request):
    return render(request, template_name="about.html")

def BusList(request):
    start = request.GET['source']
    end = request.GET['dest']
    date = request.GET['date']
    queryset = Working_days.objects.filter(day__exact=date)
    result = []
    for day in queryset:
        count = 0
        start_order = -1
        end_order = -1
        start_point = None
        end_point = None
        points = day.bus.route.points.filter(
            Q(place=start) | Q(place=end))
        for point in points:
            count += 1
            if point.place.id == int(start):
                start_order = point.order
                start_point = point
            if point.place.id == int(end):
                end_order = point.order
                end_point = point

        if count == 2 and (start_order < end_order):
            cost = day.bus.cost_per_km * (end_point.distance - start_point.distance)
            result.append(dict(WorkingDaySerializer(day).data,
                               **{"start": PointSerializer(start_point).data, "end": PointSerializer(end_point).data,
                                  "cost": cost}))

    context = {"buses": result}

    return render(request, template_name="buslist.html", context=context)


# @parser_classes([FormParser, MultiPartParser])
@login_required(login_url="/login")
@csrf_exempt
def BookBus(request):
    data = request.POST
    print(data)
    id = data.get('id')
    seats = data.getlist('seats')
    names = data.getlist('name')
    ages = data.getlist('age')
    genders = data.getlist('gender')
    to = data.get('to')
    fro = data.get('fro')

    if not id or not seats or not to or not fro:
        return HttpResponseBadRequest("Sufficient data not sent")

    day = Working_days.objects.filter(id=id).all()[0]
    to_point = Points.objects.get(id=to)
    fro_point = Points.objects.get(id=fro)
    if fro_point.route != to_point.route:
        return HttpResponseBadRequest("To and from are from different routes.")
    print(fro_point.route.bus_route)
    # if fro_point.route.bus_route != day.bus:
    #     return HttpResponseBadRequest("Invalid points.")

    bus_day = WorkingDaySerializer(day).data

    if bus_day['available_seats'] == 0:
        return HttpResponseBadRequest("No available seats")

    for seat in seats:
        if int(seat) > bus_day['available_seats']:
            return HttpResponseBadRequest("Invalid seat selected.")
        if Ticket.objects.filter(day=id, no=seat).exists():
            return HttpResponseBadRequest("Already booked seat selected.")

    tickets = []
    for i, seat in enumerate(seats):
        traveller = Traveller(name=names[i], age=ages[i], gender=genders[i])
        traveller.save()
        ticket = Ticket(traveller=traveller, day=day, to=to_point, fro=fro_point, no=seat, booked_by=request.user)
        ticket.save()
        tickets.append(TicketSerializer(ticket).data)
    return render(request, template_name="busbooked.html", context={"tickets": tickets})

@login_required(login_url="/login")
def SelectBus(request):
    id = request.GET.get('id', None)
    to = request.GET.get('to', None)
    fro = request.GET.get('fro', None)

    try:
        bus_day = Working_days.objects.filter(id=id).all()[0]
        to_point = Points.objects.get(id=to)
        fro_point = Points.objects.get(id=fro)
    except:
        return HttpResponseBadRequest("Invalid details")
    if fro_point.route != to_point.route:
        return HttpResponseBadRequest("To and from are from different routes.")
    # if fro_point.route.bus_route != bus_day.bus:
    #     return HttpResponseBadRequest("Invalid points.")

    cost = bus_day.bus.cost_per_km * (to_point.distance - fro_point.distance)
    return render(request, template_name="selectbus.html",
                  context=dict(WorkingDayDetailedSerializer(bus_day).data, **{'to': to, 'fro': fro, 'cost': cost}))


@login_required(login_url="/login")
def Tickets(request):
    tickets = Ticket.objects.filter(booked_by=request.user).all()

    return render(request, template_name="tickets.html",
                  context={"tickets": [TicketSerializer(ticket).data for ticket in tickets]})


@login_required(login_url="/login")
def TicketCancel(request):
    tickets = Ticket.objects.filter(booked_by=request.user, id=request.GET.get('id')).all()
    tickets[0].delete()
    return redirect("/home/tickets")


def view_404(request, exception=None):
    return redirect('/home')


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'working_day__day': ['exact', 'lte', 'gte'], 'route__fro': [
        'icontains'], 'route__to': ['icontains']}


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='book')
    def book(self, request):
        to = Points.objects.filter(id=request.data['to'])
        fro = Points.objects.filter(id=request.data['fro'])
        day = Working_days.objects.filter(id=request.data['day'])

        if (to.exists() and fro.exists() and day.exists()):
            capacity = day.all()[0].bus.capacity
            print(capacity)
        else:
            raise HttpResponseBadRequest()
