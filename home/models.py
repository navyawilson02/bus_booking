from pyexpat import model
from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
bustype = [('NO', 'nonAC'),
           ('AC', 'Multiaxle Volvo'),
           ('SL', 'AC Sleeper'),
           ('AI', 'Airbus')
           ]

gender = [('M', 'Male'),
          ('F', 'Female'),
          ('O', 'Other'),
          ]


class Traveller(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(choices=gender, max_length=3)

    def __str__(self):
        return f'{self.id}:{self.name}'


class Route(models.Model):

    fro = models.CharField(max_length=20)
    to = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.id}:{self.fro}-{self.to}'


class Bus(models.Model):

    no = models.CharField(max_length=20, unique=True)
    type = models.CharField(choices=bustype, max_length=3)
    capacity = models.IntegerField()
    route = models.OneToOneField(
        Route, related_name='bus_route', on_delete=models.CASCADE)
    cost_per_km = models.IntegerField()

    def __str__(self):
        return f'{self.id}:{self.no}'


class Stops(models.Model):
    # [TODO] add details
    place = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.id}:{self.place}'


class Points(models.Model):
    order = models.IntegerField()
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name='points')
    distance = models.IntegerField()
    time = models.TimeField()
    place = models.ForeignKey(
        Stops, on_delete=models.RESTRICT, related_name='bus_points')

    def __str__(self):
        return f"{self.id}-{self.route.__str__()}::{self.order}"

    class Meta:
        unique_together = ['route', 'id']


class Working_days(models.Model):
    day = models.DateField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE,
                            related_name='working_day')

    def __str__(self):
        return f'{self.id}:bus({self.bus})'


class Ticket(models.Model):
    day = models.ForeignKey(
        Working_days, on_delete=models.CASCADE, related_name='seat')
    no = models.CharField(max_length=20)
    fro = models.ForeignKey(
        Points, on_delete=models.RESTRICT, related_name="ticket_from")
    to = models.ForeignKey(
        Points, on_delete=models.RESTRICT, related_name="ticket_to")
    traveller = models.ForeignKey(Traveller, on_delete=models.CASCADE)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        print(self.day.bus.route.points)
        raise ValidationError('To and from are from different routes.')
        # if (self.fro.route != self.to.route):# or (self.day.bus.route != self.to.fro):
        #     raise ValidationError('To and from are from different routes.')
        #
