from django.contrib import admin
from django.urls import path, re_path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ---------------- HOME / SEARCH ----------------
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('home/', views.home_page, name='home'),  # Navbar Home link
    # ---------------- MOVIES ----------------
    path('movies/', views.movies, name='movies'),
    path('movies/<slug:slug>/', views.movie_detail, name='movie_detail'),
    path('seats/<slug:slug>/', views.seats, name='seats'),  # corrected to match your URL
    path('payment/', views.payment, name='payment'),
    path('payment/success/', views.payment_success_movie, name='payment_success'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('ticket/download/<int:booking_id>/', views.download_ticket, name='download_ticket'),

    # ---------------- STREAM ----------------
    path('stream/', views.stream, name='stream'),
    path('stream/details/', views.stream_details, name='stream_details'),
    path('stream/payment/', views.stream_payment, name='stream_payment'),
    path('stream/payment/success/', views.stream_payment_success, name='stream_payment_success'),
    path('stream/watch/<slug:movie>/', views.stream_watch, name='watch_stream'),


    # ---------------- EVENTS ----------------
    path('events/', views.events_home, name='events'),
    path('events/category/<str:category>/', views.event_category, name='event_category'),
    path('events/<str:event_id>/', views.event_details, name='event_details'),
    path('events/<str:event_id>/payment/', views.event_payment, name='event_payment'),
    path('events/payment/success/', views.event_payment_success, name='event_payment_success'),

    # ---------------- PLAYS ----------------
    path('plays/', views.plays, name='plays'),
    path('plays/payment/', views.play_payment, name='play_payment'),
    path('plays/payment/success/', views.play_payment_success, name='play_payment_success'),

    # ---------------- STATIC PAGES ----------------
    path('about/', views.about, name='about'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('profile/', views.profile, name='profile'),

    # ---------------- BOOKINGS ----------------
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('my_bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('my_bookings/ticket/', views.ticket, name='ticket'),

    # ---------------- AUTH ----------------
    path('signup/', views.signup_view, name='signup'),
    path('signup/otp_verify/', views.signup_otp_verify, name='otp_verify'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ---------------- OTP LOGIN ----------------
    path('otp_login/', views.otp_login_request, name='otp_login'),
    path('otp_login/verify/', views.otp_login_verify, name='otp_login_verify'),
]
