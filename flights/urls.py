from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .views import custom_logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path("flights/", views.index, name="index"),
    path("flights/<int:flight_id>/", views.flight_detail, name="flight_detail"),
    path("flights/<int:flight_id>/book/", login_required(views.book_flight), name="book_flight"),
    path("booking/<uuid:booking_code>/", views.booking_confirmation, name="booking_confirmation"),
    path("manage-booking/", views.manage_booking, name="manage_booking"),
    path("airports/<int:airport_id>/", views.airport_detail, name="airport_detail"),
    path("find_bookings/", views.find_bookings, name="find_bookings"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', custom_logout_view, name='logout'),
    path('guest-flights/', views.guest_flights, name='guest_flights'),
    path('promo-seen/', views.promo_seen, name='promo_seen'),

    path('api/flights/', views.api_flight_list, name='api_flight_list'),
    path('api/flights/<int:flight_id>/', views.api_flight_detail, name='api_flight_detail'),
    path('api/bookings/', views.api_create_booking, name='api_create_booking'),
]
