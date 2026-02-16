from django.contrib import admin
from .models import Booking, Movie

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "booking_type", "movie", "seats", "price", "date")
    list_filter = ("booking_type", "date")
    search_fields = ("user__username", "movie__title")

admin.site.register(Movie)
