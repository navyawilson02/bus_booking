from django.contrib import admin
from .models import *
# Register your models here.

class PointsInline(admin.TabularInline):
    model = Points

class RoutesAdmin(admin.ModelAdmin):
    model = Route
    inlines = [
        PointsInline
    ]
admin.site.register(Traveller)
admin.site.register(Bus)
admin.site.register(Route, RoutesAdmin)
admin.site.register(Points)
admin.site.register(Ticket)
admin.site.register(Working_days)
admin.site.register(Stops)

