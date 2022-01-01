from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.http import HttpResponse, request
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from mainapp.models import Customer, TruckDriver, Item, Booking, City, Truck, ItineraryTD
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import requests
from collections import Counter
import datetime, time
from django.core.mail import send_mail

@login_required
def hello_ct(request):
    return render(request, 'mainapp/index_ct.html', {})
@login_required
def hello_td(request):
    all_bookings = Booking.objects.all()
    pickup_tops = count_most_visited_city_start(all_bookings)
    dropoff_tops = count_most_visited_city_end(all_bookings)
    return render(request, 'mainapp/index_td.html', {"pickup_tops":pickup_tops, "dropoff_tops":dropoff_tops})

@login_required
def reportpb_ct(request):
    return render(request, 'mainapp/reportpb_ct.html', {})
@login_required
def reportpb_td(request):
    return render(request, 'mainapp/reportpb_td.html', {})
@login_required
def pbsuccess_ct(request):
    return render(request, 'mainapp/pbsuccess_ct.html', {})
@login_required
def pbsuccess_td(request):
    return render(request, 'mainapp/pbsuccess_td.html', {})

def signin(request):
    return render(request, 'mainapp/signin.html', {})
def signin_ct(request):
    return render(request, 'mainapp/signin_ct.html', {})
def signin_td(request):
    return render(request, 'mainapp/signin_td.html', {})

def signin_submit_td(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return render(request, 'mainapp/signin_success_td.html', {})
        else:
            # Return an 'invalid login' error message.
            return render(request, 'mainapp/signin_td.html', {'error': True})
    else:
        return render(request, 'mainapp/signin_td.html', {})

def signin_submit_ct(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return render(request, 'mainapp/signin_success_ct.html', {})
        else:
            # Return an 'invalid login' error message.
            return render(request, 'mainapp/signin_ct.html', {'error': True})
    else:
        return render(request, 'mainapp/signin_ct.html', {})


def signup(request):
    return render(request, 'mainapp/signup.html', {})
def signup_ct(request):
    if request.method == 'POST':
        error = False

        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        contactNo = request.POST['contactNo']

        if username == "" or password == "" or email == "" or first_name == "" or contactNo=="":
            error = True
        
  
        if error:
            return render(request, 'mainapp/signup.html', {
                "error": error
            })
        else:
            u = User.objects.create_user(username, email, password)
            u.first_name = first_name
            u.last_name = last_name
            u.save()

            p = Customer(user=u, contactNo = contactNo)
            p.save()

            return render(request, 'mainapp/signupsuccess.html', {})
        
    else:
        return render(request, 'mainapp/signup_ct.html', {})

def signup_td(request):
    if request.method == 'POST':
        error = False

        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        contactNo = request.POST['contactNo']
        drivingLicenceNo = request.POST['drivingLicenceNo']

        if username == "" or password == "" or email == "" or first_name == "" or last_name == "" or contactNo == "" or drivingLicenceNo == "":
            error = True
        
  
        if error:
            return render(request, 'mainapp/signup.html', {
                "error": error
            })
        else:
            u = User.objects.create_user(username, email, password)
            u.first_name = first_name
            u.last_name =last_name
            u.save()

            p = TruckDriver(user=u, contactNo=contactNo, drivingLicenceNo=drivingLicenceNo)
            p.save()

            return render(request, 'mainapp/signupsuccess.html', {})
        
    else:
        return render(request, 'mainapp/signup_td.html', {})

def signout(request):
    logout(request)
    return render(request, 'mainapp/signin.html', { "logout": True })

@login_required
def addressbook_ct(request):
    cities = City.objects.all()
    return render(request, 'mainapp/addressbook_ct.html', {"cities": cities})
@login_required
def addressbook_td(request):
    cities = City.objects.all()
    return render(request, 'mainapp/addressbook_td.html', {"cities": cities})

@login_required
def account_ct(request):
    p = Customer.objects.get(user=request.user)

    return render(request, 'mainapp/account_ct.html', {"profile": p})

@login_required
def account_td(request):
    p = TruckDriver.objects.get(user=request.user)
    #CHANGE
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        p.drivinglicence = myfile
        p.save()
        return render(request, 'mainapp/account_td.html', {"profile": p, "uploaded": True})

    return render(request, 'mainapp/account_td.html', {"profile": p})

@login_required
def remove_picture(request):
    p = TruckDriver.objects.get(user=request.user)
    p.drivinglicence = None
    p.save()
    return redirect('mainapp:account_td')

@login_required
def delete_booking(request, booking_id):
    b = Booking.objects.get(pk=booking_id)
    b.delete()
    return redirect('mainapp:mybookings')

@login_required
def delete_itinerary(request, itinerary_id):
    i = ItineraryTD.objects.get(pk=itinerary_id)
    i.delete()
    return redirect('mainapp:alldeliveries')

@login_required
def delete_item(request, item_id):
    i = Item.objects.get(pk=item_id)
    i.delete()
    return redirect('mainapp:mybookings')

@login_required
def delete_itinerary(request, itinerary_id):
    i = ItineraryTD.objects.get(pk=itinerary_id)
    i.delete()
    return redirect('mainapp:alldeliveries')

@login_required
def add_item(request):
    customer = Customer.objects.get(user=request.user)
    bookings = Booking.objects.filter(customer=customer)
    if request.method == 'POST':
        error = False
        b = request.POST['booking']
        booking = Booking.objects.get(pk=b)
        size = request.POST['size']
        weight = request.POST['weight']
        description = request.POST['description']
        volume = request.POST['volume']
        price = request.POST['price']

        if size == "" or booking == "" or weight == "" or description == "" or volume == "" or price == "":
            error = True
        
  
        if error:
            return render(request, 'mainapp/add_item.html', {
                "error": error, "bookings": bookings
            })
        else:
            i = Item.objects.create()
            i.booking = booking
            i.size = size
            i.volume = volume
            i.weight = weight
            i.description = description
            i.price = price
            i.save()
            booking.full_price = float(booking.full_price) + float(price)
            booking.full_volume = float(booking.full_volume) + float(volume)
            booking.save()

            return render(request, 'mainapp/add_item_success.html', {})
        
    else:
        return render(request, 'mainapp/add_item.html', {"bookings": bookings})
    
@login_required
def booking(request):
    cities = City.objects.all()
    if request.method == 'POST':
        error = False
        pickUpLocation = request.POST['pickUpLocation']
        dropOffLocation = request.POST['dropOffLocation']
        pickUpDate = request.POST['pickUpDate']
        dropOffDate = request.POST['dropOffDate']
        customer = Customer.objects.get(user=request.user)

        if dropOffLocation == "" or pickUpLocation == "" or pickUpDate == "" or dropOffDate == "":
            error = True
  
        if error:
            return render(request, 'mainapp/booking.html', {"error": error, "cities": cities})
        else:
            pickUp = City.objects.get(city_name=pickUpLocation)
            dropOff = City.objects.get(city_name=dropOffLocation)
            b = Booking.objects.create(customer=customer, pickUpLocation = pickUp, dropOffLocation = dropOff, pickUpDate = pickUpDate, dropOffDate = dropOffDate)

            return render(request, 'mainapp/booking_success.html', {})
        
    else:
        return render(request, 'mainapp/booking.html', {"cities": cities})

@login_required
def mybookings(request): 
    customer = Customer.objects.get(user=request.user)
    bookings = Booking.objects.filter(customer=customer)
    items = Item.objects.all()
    trucks = Truck.objects.all()
    return render(request, 'mainapp/mybookings.html', {"bookings": bookings, "items":items, "trucks":trucks})

@login_required
def mytruck(request): 
    td = TruckDriver.objects.get(user=request.user)
    truck = Truck.objects.filter(truckDriver=td)
    exist = False
    if (truck.exists()): 
        exist = True
        truck= truck[0]
    
    if request.method == 'POST':
        error = False
        plateNo = request.POST['plateNo']
        policyNo = request.POST['policyNo']
        model = request.POST['model']
        productionYear = request.POST['productionYear']
        mileage = request.POST['mileage']
        volume = request.POST['volume']
        max_capacity = request.POST['max_capacity']

        if plateNo == "" or policyNo == "" or model == "" or productionYear == "" or mileage == "" or volume == "" or max_capacity == "":
            error = True
        if error:
            return render(request, 'mainapp/mytruck.html', {"error": error, "truck": truck, "exist": exist})

        else:
            t = Truck.objects.create(truckDriver = td, plateNo = plateNo,policyNo = policyNo,model = model,productionYear = productionYear, mileage = mileage, volume = volume, max_capacity = max_capacity)
            #t.save()

            return render(request, 'mainapp/mytruck_add_success.html', {"truck": truck, "exist": True})
        
    else:
        return render(request, 'mainapp/mytruck.html', {"truck": truck, "exist": exist})
    
@login_required
def newdelivery(request):
    td = TruckDriver.objects.get(user=request.user)
    truck_td = Truck.objects.filter(truckDriver=td)
    #add error message if truck not added
    truck_error=False
    if truck_td.count()==0:
        return render(request, 'mainapp/pls_add_truck_error.html', {})
    truck = truck_td[0]
    cities = City.objects.all()
    if request.method == 'POST':
        error = False
        dd = request.POST['departureDate']
        ad = request.POST['arrivalDate']
        departure_l = request.POST['departureLocation']
        dl = City.objects.filter(city_name=departure_l)[0]
        arrival_l = request.POST['arrivalLocation']
        al = City.objects.filter(city_name= arrival_l)[0]
        rv = request.POST['remainingVolume']

        if dd == "" or ad == "" or dl == "" or al == "" or rv == "":
            error = True
        if error:
            return render(request, 'mainapp/newdelivery.html', { "error": error, "cities": cities, "truck": truck })
        else:
            i = ItineraryTD.objects.create(truckDriver=td, departureDate= dd, arrivalDate=ad, departureLocation=dl, arrivalLocation=al, remainingVolume = rv)
            return render(request, 'mainapp/newdelivery_success.html', {})
        
    else:
        return render(request, 'mainapp/newdelivery.html', {"cities": cities, "truck": truck})

@login_required
def alldeliveries(request): 
    td = TruckDriver.objects.get(user=request.user)
    itineraries = ItineraryTD.objects.filter(truckDriver=td)
    stops = Booking.objects.all().order_by('pickUpDate')
    return render(request, 'mainapp/alldeliveries.html', {"itineraries": itineraries, "stops" : stops})
@login_required
def input_time(request, booking):
    b = Booking.objects.get(pk=booking)
    if request.method == 'POST':
        pickup = request.POST['pickup']
        dropoff = request.POST['dropoff']
        b.pickup_time = pickup
        b.dropoff_time = dropoff
        b.save()
        return redirect('mainapp:alldeliveries')
    return render(request, 'mainapp/input_time.html', {"booking": b})


@login_required
def td_select_booking(request, itinerary):
    td = TruckDriver.objects.get(user=request.user)
    i = get_object_or_404(ItineraryTD, pk=itinerary)
    bookings = Booking.objects.filter(assigned=False)
    bookings = filter_matching_dates(bookings, i)
    bookings = list(bookings)
    eligible_b = eligible_bookings(bookings, i)
    other_bookings = difference(bookings, list(eligible_b))

    truck=Truck.objects.get(truckDriver=td)
    vol_others = total_volume_bookings(bookings)
    return render(request, 'mainapp/td_select_booking.html', {"eligible_bookings": list(eligible_b), "rest": list(other_bookings), "itinerary": i, "truck": truck, "vol_others": vol_others })

@login_required
def td_take_booking(request, itinerary, booking):
    b = Booking.objects.get(pk=booking)
    i = ItineraryTD.objects.get(pk=itinerary)
    b.td_itinerary = i
    b.assigned = True
    i.remainingVolume = float(i.remainingVolume) - float(compute_booking_volume(booking))
    b.save()
    customer = b.customer
    email = customer.user.email
    send_mail(
                'Your booking is successful!',
                'Dear '+ (customer.user.first_name) +' \n\nA truck driver has taken your booking!\n\nLogin to see the time of pickup and dropoff. \n\nBooking details: '+ (b.pickUpLocation.city_name) +' to '+(b.dropOffLocation.city_name) +' on the '+ str(b.pickUpDate) + '/' + str(b.dropOffDate) +'.',
                'truckpool.webapp@gmail.com',
                [email],
                fail_silently=False,
            )
    return render(request, 'mainapp/td_take_booking.html', {"id": itinerary})

@login_required
def load_truck(request, itinerary):
    i = ItineraryTD.objects.get(pk=itinerary)
    td = i.truckDriver
    truck = Truck.objects.get(truckDriver = td)
    print(truck)
    #cargos with latest dropoff should go first in the truck
    b = Booking.objects.filter(td_itinerary=i).order_by('-dropOffDate')
    bookings = list(b)
    last_dropoffs = cargos_booking_list(bookings)
    cargos = last_dropoffs
    heaviest = heaviest_first(cargos)
    largest = largest_first(cargos)
    space_ut = space_utilization_bookings(bookings, i)
    return render(request, 'mainapp/load_truck.html', {"last_dropoffs": last_dropoffs, "bookings": b, "space_ut": space_ut, "largests":largest, "heaviests": heaviest, "itinerary": i, "truck": truck})

@login_required
def see_all_itineraries(request): 
    itineraries = ItineraryTD.objects.all()
    tds = TruckDriver.objects.all()
    return render(request, 'mainapp/see_all_itineraries.html', {"itineraries": itineraries, "tds": tds})

'''_______________________________Optimization algorithms______________________________________'''

def eligible_bookings(all_bookings, truck_itinerary):
    eligible_bookings=[]
    start_td = truck_itinerary.departureLocation
    end_td = truck_itinerary.arrivalLocation

    t_end = time.time() + 60 * 1 #1min * 60 seconds = 60 sec
    
    while time.time() < t_end:
        if len(all_bookings)==0: #if booking list is empty stop 
            break
        #step 1: get bookings with same departure location + add them to eligible, remove them from all_bookings
        pickup_is_current_start = pickup_is(start_td, all_bookings)
        if len(pickup_is_current_start)>0:
            eligible_bookings.extend(list(pickup_is_current_start))
            all_bookings = difference(all_bookings, pickup_is_current_start)
        if len(all_bookings)==0:
            break
        #step 2: get bookings with same dropOff location + add them to eligible, remove them from all_bookings
        dropOff_is_current_end = dropoff_is(end_td, all_bookings)
        if len(dropOff_is_current_end)>0:
            eligible_bookings.extend(list(dropOff_is_current_end))
            all_bookings = difference(all_bookings, dropOff_is_current_end)
        if len(all_bookings)==0:
            break
        #step 3: get booking with pickUp that is the closest to the departure of TD + add it to eligible, remove it from all_bookings
        closest_location = closest_to(start_td, all_bookings)
        eligible_bookings.extend(list(closest_location))
        all_bookings = difference(all_bookings, closest_location)
        if len(all_bookings)==0:
            break
        #step 4: get bookings with dropoff same as closest.dropOff + add them to eligible, remove them from all_bookings
        dropoff_is_current_start = dropoff_is(closest_location[0].dropOffLocation, all_bookings)
        if len(dropoff_is_current_start)>0:
            eligible_bookings.extend(list(dropoff_is_current_start))
            all_bookings = difference(all_bookings, dropoff_is_current_start)
        if len(all_bookings)==0:
            break
        #step 5: replace TD current position with the pickUp location of the closest-start-booking
        start_td = closest_location[0].pickUpLocation
    return eligible_bookings #returns array [] of bookings

#returns list 1 without elements of list 2
def difference(list1, list2):
    set_difference = set(list1) - set(list2)
    list_difference = list(set_difference)
    return list_difference

#only display the bookings matching the itinerary dates
def filter_matching_dates(bookings, itinerary):
    depart_date = itinerary.departureDate
    arrival_date = itinerary.arrivalDate
    filtered=[]
    for i in range(bookings.count()):
        booking=bookings[i]
        if booking.pickUpDate>=depart_date and booking.dropOffDate<=arrival_date:
            filtered.append(booking)
    return filtered

#get booking that has the closest pickUp location to "start"-location
def closest_to(start, all_bookings):
    closest = all_bookings[0]
    distance_min = compute_distance(start, closest.pickUpLocation)
    for i in range(1, len(all_bookings)):
        booking= all_bookings[i]
        distance_local = compute_distance(start, booking.pickUpLocation.city_name)
        if distance_local<distance_min:
            closest=all_bookings[i]
            distance_min=distance_local
    closest = Booking.objects.filter(pk=closest.id)
    return closest

#get list bookings where pickUp location is the same as "start"-location
def pickup_is(start, all_bookings):
    satisfy_rq=[]
    for i in range(len(all_bookings)):
        booking = all_bookings[i]
        if booking.pickUpLocation == start:
            satisfy_rq.append(booking)
    #sort in order that is closest to td arrival sort_closest_to_end(satisfy_rq, end_td)- change
    return satisfy_rq

#get list bookings where dropOff location is the same as "arrival"-location
def dropoff_is(arrival, all_bookings):
    satisfy_rq=[]
    for i in range(len(all_bookings)):
        booking = all_bookings[i]
        if booking.dropOffLocation == arrival:
            satisfy_rq.append(booking)
    #sort in order that is closest to td arrival sort_closest_to_end(satisfy_rq, end_td)- change
    return satisfy_rq


#computes vol(1 booking)/vol(truck) in %
def space_utilization_1(booking, itinerary):
    truck = get_object_or_404(Truck, truckDriver=itinerary.truckDriver)
    truck_vol = truck.volume
    booking_vol = compute_booking_volume(booking)
    ratio = (booking_vol/truck_vol)
    val = round(ratio, 2)
    return val*100

#computes total volume of array of bookings
def total_volume_bookings(bookings):
    #bookings = Booking.objects.filter(td_itinerary=itinerary)
    #bookings = list(bookings)
    val = 0
    for i in range(len(bookings)):
        booking = bookings[i]
        val= val + compute_booking_volume(booking)
    return val

#computes vol(bookings)/vol(truck) in %
def space_utilization_bookings(bookings, itinerary):
    truck = get_object_or_404(Truck, truckDriver=itinerary.truckDriver)
    truck_vol = truck.volume
    bookings_vol = total_volume_bookings(bookings)
    ratio = (bookings_vol/truck_vol)
    value = ratio*100
    val = round(value, 2)
    return val

#compute distance between two cities
def compute_distance(origin, destination):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    payload = {
        'mode':'driving',
        'units':'metric',
        'origins': origin,
        'destinations': destination,
        'key': "AIzaSyD-ew0bRZzGvqXm_OkyctMfGJvzaZdtQG0",

    }
    
    r = requests.get(url, params=payload)
    response = r.json()
    distance = response['rows'][0]['elements'][0]['distance']['value']/1000
    return distance

#compute total volume of all the items in a booking
def compute_booking_volume(booking):
    items = Item.objects.filter(booking = booking)
    vol = 0
    for i in range(items.count()):
        item = items[i]
        vol += item.volume
    return vol

#compute total weight of all the items in a booking
def compute_booking_weight(booking):
    items = Item.objects.filter(booking = booking)
    weight = 0
    for i in range(items.count()):
        item = items[i]
        weight += item.weight
    return weight

#returns all the items of several bookings of an itinerary
def items_of_allbookings(itinerary):
    items=[]
    bookings = Booking.objects.filter(td_itinerary=itinerary)
    for i in range(bookings.count()):
        booking = bookings[0]
        item = Item.objects.filter(booking=booking)
        for j in range(item.count()):
            items.append(item[j])
    return items


#returns ordered set of cargos accrding to the weight/volume and the date of drop off
def space_opt(bookings, itinerary):
    ordered=[]
    cargos = cargos_booking_list(bookings)
    while len(cargos)>0:
        cargo = get_heaviest(cargos)
        ordered.append(cargo)
    return ordered #return list of bookings where order matters: first one should be put first

def largest_first(cargos):
    largest = sorted(cargos, key=lambda x: x.volume, reverse=True)
    return largest
def heaviest_first(cargos):
    heaviest = sorted(cargos, key=lambda x: x.weight, reverse=True)
    return heaviest

#returns heaviest cargo of the array of the cargos
def get_heaviest(cargos):
    heaviest = cargos[0]
    for i in range(1, len(cargos)):
        if heaviest.weight<cargos[i].weight:
            heaviest = cargos[i]
    return heaviest
#returns largest cargo of the array of the cargos
def get_largest(cargos):
    largest = cargos[0]
    for i in range(1, len(cargos)):
        if largest.volume<cargos[i].volume:
            largest = cargos[i]
    return largest

#returns list of all cargos of a booking
def cargos_booking_list(bookings):
    cargos=[]
    for i in range(len(bookings)):
        booking = bookings[i]
        items = Item.objects.filter(booking=booking)
        for j in range(items.count()):
            cargos.append(items[j])
    return cargos

#get cities with the highest demand for start location
def count_most_visited_city_start(all_bookings):
    start_locations=[]
    for i in range(all_bookings.count()):
        start_locations.append(all_bookings[i].pickUpLocation)
    counter = Counter(start_locations).most_common() #returns [('Paris', 7), ('London', 5), ('Prague', 3), ... ]
    #counter = sorted(counter, key=counter.get, reverse=True) #returns ['Paris', 'London', 'Prague']
    return counter 

def count_most_visited_city_end(all_bookings):
    end_locations=[]
    for i in range(all_bookings.count()):
        end_locations.append(all_bookings[i].dropOffLocation)
    counter = Counter(end_locations).most_common() #returns [('Paris', 7), ('London', 5), ('Prague', 3), ... ]
    #counter = sorted(counter, key=counter.get, reverse=True) #returns ['Paris', 'London', 'Prague']
    return counter 
