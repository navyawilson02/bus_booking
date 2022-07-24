from pyexpat import model
from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
bustype =[('NO','nonAC'),
  ('AC', 'Multiaxle Volvo'),
  ('SL','AC Sleeper'),
  ('AI','Airbus')
  ]

class Route(models.Model):

      fro = models.CharField(max_length=20)
      to=models.CharField(max_length=20)
      cost_per_km = models.IntegerField()

      def __str__(self):
        return f'{self.id}:{self.fro}-{self.to}'

class Bus(models.Model):

    no = models.CharField(max_length=20, unique=True)
    type=models.CharField(choices=bustype,max_length=3)
    capacity=models.IntegerField()
    route=models.ForeignKey(Route,related_name='bus_route' ,on_delete=models.SET_NULL,unique=True, null=True)
    def __str__(self):
        return f'{self.id}:{self.no}'


class Points(models.Model):
    order= models.IntegerField()
    route= models.ForeignKey(Route,on_delete=models.CASCADE)
    distance=models.IntegerField()
    time=models.TimeField()
    place = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.id}-{self.route.__str__()}::{self.order}"


    class Meta:
        unique_together= ['route','id']


class Working_days(models.Model):
    day=models.DateField()
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE, related_name='working_day')

class Seats(models.Model):
    day=models.ForeignKey(Working_days,on_delete=models.CASCADE)
    no=models.CharField(max_length=20)

class Ticket(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  fro=models.ForeignKey(Points,on_delete=models.RESTRICT, related_name="ticket_from")
  to=models.ForeignKey(Points,on_delete=models.RESTRICT, related_name="ticket_to")
  seat=models.ForeignKey(Seats,on_delete=models.RESTRICT,unique=True)
  def clean(self):
        if self.fro.route != self.to.route:
            raise ValidationError('To and from are from different routes.')
  
    


