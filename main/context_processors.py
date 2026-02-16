from .models import Booking

def my_bookings(request):
    if request.user.is_authenticated:
        return {"my_bookings_count": request.user.booking_set.count()}
    return {}