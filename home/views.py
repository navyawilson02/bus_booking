from django.shortcuts import render
from rest_framework import viewsets, filters
import django_filters
from .models import *
from .serializer import BusSerializer, TicketSerializer, WorkingDaySerializer
from rest_framework.decorators import action
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
# Create your views here.

#@login_required(login_url="/login")
def HomePage(request):
    context = {}
    context["home_name"] = "Sunith vs"
    context["places"] = ["Eranakulam", "Kozhikode", "Trivandrum", "Bangalore"]
    return render(request, template_name="home.html",context=context)

def BusList(request):
    start = request.GET['source']
    end = request.GET['dest']
    date = request.GET['date']
    queryset = Working_days.objects.filter(day__exact= date, bus__route__fro__icontains = start, bus__route__to__icontains = end )

    context = {"buses":[WorkingDaySerializer(bus).data for bus in queryset]}

    return render(request, template_name="buslist.html",context=context)

@login_required(login_url="/login")
def BookBus(request):
    id = request.GET['id']
    return render(request, template_name="busbooking.html",)



class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'working_day__day': ['exact', 'lte', 'gte'], 'route__fro':['icontains'], 'route__to': ['icontains']}

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='book')
    def book(self, request):
        to = Points.objects.filter(id=request.data['to'])
        fro = Points.objects.filter(id=request.data['fro'])
        day = Working_days.objects.filter(id = request.data['day'])

        if(to.exists() and fro.exists() and day.exists()):
            capacity = day.all()[0].bus.capacity
            print(capacity)
        else:
            raise HttpResponseBadRequest()
            

