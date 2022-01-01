from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class TruckDriver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contactNo = models.CharField(max_length=15)
    drivingLicenceNo = models.CharField(max_length=30)
    #rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=5)
    #is_td = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    drivinglicence = models.ImageField(upload_to='drivingLicences', blank=True)
    picture = models.ImageField(upload_to='drivingLicences', blank=True)
    def __str__(self):
        full_name = self.user.first_name + self.user.last_name
        return full_name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contactNo = models.CharField(max_length=15, null=True, blank=True)
    #is_td = models.BooleanField(default=False)
    def __str__(self):
        full_name = self.user.first_name 
        return full_name

class Truck(models.Model):
    truckDriver = models.OneToOneField(TruckDriver, on_delete=models.CASCADE)
    plateNo = models.CharField(max_length=15, null=True)
    model = models.CharField(max_length=30, null=True)
    productionYear = models.PositiveIntegerField(validators=[MinValueValidator(1975), MaxValueValidator(2021)], null=True)
    mileage = models.PositiveIntegerField(null=True)
    policyNo = models.CharField(max_length=50, null=True)
    volume = models.DecimalField(max_digits=1000, decimal_places=2, null=True)
    max_capacity = models.DecimalField(max_digits=1000, decimal_places=2, null=True)
    '''TRUCK_SIZES = (
        ('N', 'Non Applicable'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    size = models.CharField(
        max_length=1,
        choices=TRUCK_SIZES,
        default='N',
    )'''


class City(models.Model):
    city_name = models.CharField(max_length=200)
    address = models.TextField(null=True)
    def __str__(self):
        return self.city_name

class ItineraryTD(models.Model):
    truckDriver = models.ForeignKey(TruckDriver, models.SET_NULL, null=True)
    departureDate = models.DateField(default=datetime.date.today)
    arrivalDate = models.DateField(default=datetime.date.today)
    departureLocation = models.ForeignKey(City, on_delete=models.PROTECT, null=True, related_name='departue_td')
    arrivalLocation = models.ForeignKey(City, on_delete=models.PROTECT, null=True, related_name='arrival_td')
    remainingVolume = models.DecimalField(max_digits=1000, decimal_places=2)

class Booking(models.Model):
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    pickUpLocation = models.ForeignKey(City, on_delete=models.PROTECT, null=True, related_name='pickup_ct')
    dropOffLocation = models.ForeignKey(City, on_delete=models.PROTECT, null=True, related_name='dropoff_ct')
    pickUpDate = models.DateField(default=datetime.date.today)
    dropOffDate = models.DateField(default=datetime.date.today)
    td_itinerary = models.ForeignKey(ItineraryTD, on_delete=models.CASCADE, null=True, blank=True)
    assigned = models.BooleanField(default = False)
    pickup_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    dropoff_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    full_volume = models.DecimalField(max_digits= 1000, decimal_places=2, default="0")
    full_price = models.DecimalField(max_digits= 1000, decimal_places=2, default="0")


class Item(models.Model):
    ITEM_SIZES = (
        ('N', 'Non-Applicable'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    size = models.CharField(
        max_length=15,
        choices=ITEM_SIZES,
        default='N',
    )
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    weight = models.DecimalField(max_digits= 1000, decimal_places=2, null=True)
    description = models.CharField(max_length=500, default="No description")
    volume = models.DecimalField(max_digits= 1000, decimal_places=2, null=True)
    price = models.DecimalField(max_digits= 1000, decimal_places=2, default="0")
    