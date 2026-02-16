from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# ================= MOVIE MODEL =================
class Movie(models.Model):
    title = models.CharField(max_length=200, help_text="Movie title")
    slug = models.SlugField(unique=True, blank=True)
    poster = models.CharField(max_length=300, blank=True)
    banner = models.CharField(max_length=300, blank=True)
    about = models.TextField(blank=True)
    rating = models.FloatField(default=0)
    languages = models.JSONField(default=list, blank=True)
    format = models.JSONField(default=list, blank=True)
    cast = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Movie.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def _str_(self):
        return self.title


# ================= BOOKING MODEL =================
class Booking(models.Model):
    BOOKING_TYPES = [
        ("Movie", "Movie"),
        ("Event", "Event"),
        ("Play", "Play"),
        ("Stream", "Stream"),
    ]

    STATUS_CHOICES = [
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("Used", "Used"),
        ("Pending", "Pending"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    seats = models.CharField(max_length=200, blank=True)
    show_time = models.CharField(max_length=50, blank=True, null=True)
    show_date = models.DateField(blank=True, null=True)
    price = models.FloatField(default=0)
    details = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Confirmed")

    def _str_(self):
        date_str = self.show_date.strftime("%Y-%m-%d") if self.show_date else "No Date"
        time_str = self.show_time if self.show_time else "No Time"
        return f"{self.user.username} - {self.booking_type} - {self.title} ({date_str} {time_str})"