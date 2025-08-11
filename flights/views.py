from django.shortcuts import render, get_object_or_404, redirect
from .models import Flight, Airport, Booking, Passenger
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'flights/home.html')

def guest_flights(request):
    flights = Flight.objects.all()
    return render(request, 'flights/guest_flights.html', {'flights': flights})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()

            auth_login(request, user)

            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def custom_logout_view(request):
    logout(request)
    return redirect('home')

def promo_seen(request):
    request.session['promo_code_seen'] = True
    return JsonResponse({"status": "ok"})

@api_view(['GET'])
def api_flight_list(request):
    flights = Flight.objects.all()
    from .serializers import FlightSerializer
    serializer = FlightSerializer(flights, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def api_flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    from .serializers import FlightSerializer
    serializer = FlightSerializer(flight)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def api_create_booking(request):
    from .serializers import BookingSerializer
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        flight_id = serializer.validated_data['flight_id']
        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        
        flight = get_object_or_404(Flight, id=flight_id)
        passenger, _ = Passenger.objects.get_or_create(name=name, email=email)
        booking = Booking.objects.create(passenger=passenger, flight=flight)
        
        return JsonResponse({"message": "Booking created", "booking_code": booking.booking_code})
    
    return JsonResponse(serializer.errors, status=400)



def index(request):
    flights = Flight.objects.all()
    return render(request, "flights/index.html", {"flights": flights})

def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    return render(request, "flights/flight_detail.html", {"flight": flight})

def airport_detail(request, airport_id):
    airport = get_object_or_404(Airport, id=airport_id)
    return render(request, "flights/airport_detail.html", {"airport": airport})

@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == "POST":
        name = request.user.username
        email = request.user.email

        passenger = Passenger.objects.filter(email=email).first()
        if not passenger:
            passenger = Passenger.objects.create(name=name, email=email)
        
        booking = Booking.objects.create(passenger=passenger, flight=flight)
        return redirect("booking_confirmation", booking_code=booking.booking_code)

    return render(request, "flights/book_flight.html", {"flight": flight})

def booking_confirmation(request, booking_code):
    booking = get_object_or_404(Booking, booking_code=booking_code)
    return render(request, "flights/booking_confirmation.html", {"booking": booking})

def manage_booking(request):
    if request.method == "POST":
        booking_code = request.POST["booking_code"]
        try:
            booking = Booking.objects.get(booking_code=booking_code)
            return render(request, "flights/manage_booking_result.html", {"booking": booking})
        except Booking.DoesNotExist:
            return HttpResponse("Booking code is incorrect.", status=404)
    return render(request, "flights/manage_booking_form.html")

def find_bookings(request):
    bookings = None
    if request.method == "POST":
        email = request.POST.get("email")
        passenger = Passenger.objects.filter(email=email).first()
        if passenger:
            bookings = Booking.objects.filter(passenger=passenger)
    return render(request, "flights/find_bookings.html", {"bookings": bookings})
