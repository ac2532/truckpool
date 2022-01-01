from django.contrib import admin
from mainapp.models import TruckDriver, Customer, Truck, ItineraryTD, Booking, Item, City

admin.site.register(TruckDriver)
admin.site.register(Customer)
admin.site.register(Truck)
admin.site.register(City)
admin.site.register(ItineraryTD)
admin.site.register(Booking)
admin.site.register(Item)
