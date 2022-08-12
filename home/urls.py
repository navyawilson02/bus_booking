from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusViewSet, SelectBus, TicketViewSet, HomePage, BusList, BookBus, Tickets

# Setup the URLs and include login URLs for the browsable API.
router = DefaultRouter()
router.register('bus', BusViewSet)
router.register('ticket', TicketViewSet)

urlpatterns = [
    path(r'', HomePage),
    path(r'buses/', BusList),
    path(r'book/', BookBus),
    path(r'tickets/', Tickets),
    path(r'select/', SelectBus),
    path(r'', include(router.urls)),
]
