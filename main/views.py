from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User   # ✅ ADD THIS
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from datetime import date, datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import qrcode
import io
import random

from .models import Movie, Booking


# -----------------------
# MOVIES DATABASE
# -----------------------
MOVIES = {
    "akhanda2": {
        "title": "Akhanda 2: Thaandavam",
        "banner": "assets/images/movies/akanda2.avif",
        "poster": "assets/images/movies/akanda2.avif",
        "about": "God of Masses Nandamuri Balakrishna presents Akhanda 2: Thaandavam.",
        "languages": ["Telugu", "Tamil", "English"],
        "genre": ["Action"],
        "format": ["2D"],
        "rating": "8.8/10",
        "cast": [
            {"name": "Nandamuri Balakrishna", "role": "Actor", "image": "assets/images/crew/balakrishna.avif"},
            {"name": "Samyuktha Menon", "role": "Actor", "image": "assets/images/crew/samyuktha-menon.avif"},
        ],
        "crew": [
            {"name": "Boyapati Srinu", "role": "Director", "image": "assets/images/crew/boyapati-srinu.avif"},
        ]
    },
    "avatar": {
        "title": "Avatar: Fire and Ash",
        "banner": "assets/images/movies/avatar.avif",
        "poster": "assets/images/movies/avatar.avif",
        "about": "Jake Sully and Neytiri face a new danger on Pandora.",
        "languages": ["English", "Kannada", "Malayalam"],
        "genre": ["Action", "Drama"],
        "format": ["3D"],
        "rating": "9.1/10",
        "cast": [
            {"name": "Sam Worthington", "role": "Actor", "image": "assets/images/crew/sam-worthington.avif"},
            {"name": "Zoe Saldaña", "role": "Actor", "image": "assets/images/crew/zoe-saldana.avif"}
        ],
        "crew": [
            {"name": "James Cameron", "role": "Director", "image": "assets/images/crew/james-cameron.avif"}
        ]
    },
    "salaar": {
        "title": "Salaar",
        "banner": "assets/images/movies/salar.jpg",
        "poster": "assets/images/movies/salar.jpg",
        "about": "A violent man rises in a world of crime and power.",
        "languages": ["Telugu", "Hindi", "English", "Tamil"],
        "genre": ["Action"],
        "format": ["2D"],
        "rating": "9.0/10",
        "cast": [
            {"name": "Prabhas", "role": "Actor", "image": "assets/images/crew/prabhas.jpg"},
            {"name": "Shruti Haasan", "role": "Actor", "image": "assets/images/crew/sruthi.jpg"}
        ],
        "crew": [
            {"name": "Prashanth Neel", "role": "Director", "image": "assets/images/crew/prashanth.webp"}
        ]
    },
    "pushpa": {
        "title": "Pushpa",
        "banner": "assets/images/movies/pushpa.jpg",
        "poster": "assets/images/movies/pushpa.jpg",
        "about": "Pushpa Raj rises in red sandalwood smuggling.",
        "languages": ["Telugu", "Hindi", "English", "Tamil"],
        "genre": ["Action", "Drama"],
        "format": ["2D"],
        "rating": "8.5/10",
        "cast": [
            {"name": "Allu Arjun", "role": "Actor", "image": "assets/images/crew/allu.jpg"},
            {"name": "Rashmika Mandanna", "role": "Actor", "image": "assets/images/crew/rashmika.jpg"}
        ],
        "crew": [
            {"name": "Sukumar", "role": "Director", "image": "assets/images/crew/sukumar.webp"}
        ]
    },
    "kalki": {
        "title": "Kalki 2898 AD",
        "banner": "assets/images/movies/kalki.jpg",
        "poster": "assets/images/movies/kalki.jpg",
        "about": "A futuristic mythological sci-fi epic.",
        "languages": ["Telugu", "Hindi"],
        "genre": ["Sci-Fi", "Action"],
        "format": ["2D"],
        "rating": "9.2/10",
        "cast": [
            {"name": "Prabhas", "role": "Actor", "image": "assets/images/crew/prabhas.jpg"},
            {"name": "Shruti Haasan", "role": "Actor", "image": "assets/images/crew/shruti.jpg"}
        ],
        "crew": [
            {"name": "Nag Ashwin", "role": "Director", "image": "assets/images/crew/nag.jpg"}
        ]
    },
    "tere-ishk-mein": {
        "title": "Tere Ishk Mein",
        "banner": "assets/images/movies/tere-ishk-mein.avif",
        "poster": "assets/images/movies/tere-ishk-mein.avif",
        "about": "A romantic drama.",
        "languages": ["Hindi"],
        "genre": ["Romantic", "Drama"],
        "format": ["2D"],
        "rating": "7.8/10",
        "cast": [
            {"name": "Dhanush", "role": "Actor", "image": "assets/images/crew/dhanush.webp"},
            {"name": "Kriti Sanon", "role": "Actor", "image": "assets/images/crew/kriti.jpg"}
        ],
    },
    "mowgli": {
        "title": "Mowgli",
        "banner": "assets/images/movies/mowgli.avif",
        "poster": "assets/images/movies/mowgli.avif",
        "about": "A boy raised by wolves survives the jungle.",
        "languages": ["Telugu", "Hindi"],
        "genre": ["Action", "Drama"],
        "format": ["2D"],
        "rating": "8.0/10",
        "cast": [
            {"name": "Rohan", "role": "Actor", "image": "assets/images/crew/roshan.jpg"},
            {"name": "Sakkshi Mhadolkar", "role": "Actor", "image": "assets/images/crew/sakshi.jpg"}
        ],
        "crew": [
            {"name": "Sandeep Raj", "role": "Director", "image": "assets/images/crew/sandeep.webp"}
        ]
    },
    "andhra-king": {
        "title": "Andhra King Taluka",
        "banner": "assets/images/movies/andhra-king-taluka.avif",
        "poster": "assets/images/movies/andhra-king-taluka.avif",
        "about": "A fun comedy entertainer.",
        "languages": ["Telugu", "English", "Hindi"],
        "genre": ["Comedy", "Romantic"],
        "format": ["2D"],
        "rating": "8.1/10",
        "cast": [
            {"name": "Ram Pothineni", "role": "Actor", "image": "assets/images/crew/ram.jpg"},
            {"name": "Bhagyashri Borse", "role": "Actor", "image": "assets/images/crew/bhagya.jpg"}
        ],
        "crew": [
            {"name": "Mahesh Babu", "role": "Director", "image": "assets/images/crew/mahesh.jpg"}
        ]
    }
}
BOOKED_SEATS = {slug: [] for slug in MOVIES.keys()}


# =====================================================
# HOME + SEARCH
# =====================================================

def home(request):
    return render(request, "index.html", {"movies": MOVIES})
def home_page(request):
    return render(request, "home.html")  # simple landing page

def search(request):
    q = request.GET.get("q", "").lower()

    movie_results = [(s, m) for s, m in MOVIES.items() if q in m["title"].lower()]

    event_results = []
    if "LIVE_EVENTS" in globals():
        event_results = [e for e in LIVE_EVENTS if q in e["name"].lower()]

    return render(request, "search_results.html", {
        "query": q,
        "movie_results": movie_results,
        "event_results": event_results
    })


# =====================================================
# MOVIE BOOKING FLOW
# =====================================================

def movies(request):
    return render(request, "movies.html", {"movies": MOVIES})

def movie_detail(request, slug):
    movie = MOVIES.get(slug)  # your current code uses dictionary
    # If you also have a Movie model instance:
    # movie_obj = Movie.objects.get(slug=slug)  # get the actual model with id
    return render(request, "movie_detail.html", {
        "movie": movie,
        "movies": MOVIES,
        "slug": slug
        # "movie_obj": movie_obj,  # pass it if using model
    })

BOOKED_SEATS = {}

def seats(request, slug):
    movie = MOVIES.get(slug)   # your movie dict

    lang = request.GET.get("lang")
    fmt = request.GET.get("fmt")
    show = request.GET.get("show")

    if request.method == "POST":
        selected_seats = request.POST.getlist("seats")

        price_per_seat = 150
        total_price = len(selected_seats) * price_per_seat

        # ✅ store ticket info
        request.session["ticket_data"] = {
            "movie": movie["title"],
            "theatre": "PVR Cinemas",
            "date": str(date.today()),
            "show": show,
            "seats": selected_seats,
            "total": total_price
        }

        return redirect("payment")

    return render(request, "seats.html", {
        "movie": movie,
        "show": show
    })

@login_required
def payment(request):
    ticket = request.session.get("ticket_data")
    return render(request, "payment.html", {"ticket": ticket})


@login_required
def payment_success_movie(request):
    ticket = request.session.get("ticket_data")
    if not ticket:
        messages.error(request, "No movie booking found.")
        return redirect("movies")

    booking = Booking.objects.create(
        user=request.user,
        title=ticket["movie"],
        booking_type="Movie",
        seats=len(ticket["seats"]),
        price=ticket["total"],
        date=date.today(),
        details=f"Theatre: {ticket['theatre']} | Show: {ticket['show']}"
    )

    request.session["booking_id"] = booking.id
    request.session.pop("ticket_data", None)

    return redirect("booking_success")


# ==========================
# BOOKING SUCCESS / PDF / STREAM ACCESS
# ==========================
@login_required
def booking_success(request):
    # Get booking ID from session
    booking_id = request.session.get("booking_id")
    if not booking_id:
        messages.error(request, "No booking found.")
        return redirect("home")

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    context = {
        "booking": booking,
        "booking_type": booking.booking_type,
        "title": getattr(booking, "title", "Booking"),
        "details": getattr(booking, "details", ""),
        "seats_or_tickets": getattr(booking, "seats", 1),
        "date": getattr(booking, "date", ""),
        "time": getattr(booking, "show_time", ""),
        "total": booking.price,
        "booking_id": booking.id
    }

    # Clear session key after success page
    request.session.pop("booking_id", None)

    return render(request, "booking_success.html", context)
# -----------------------
# STREAM MOVIES DATABASE
# -----------------------
STREAM_MOVIES = [
    {"title": "John Wick", "language": "English", "genre": "Action", "price": "99",
     "image": "assets/images/movies/john.avif", "desc": "A retired assassin seeks revenge.",
     "about": "John Wick is a former hitman who comes out of retirement to avenge his beloved dog."},
    {"title": "Kill Bill", "language": "English", "genre": "Action", "price": "99",
     "image": "assets/images/movies/kill.avif", "desc": "A martial arts revenge saga.",
     "about": "A former assassin seeks revenge on her ex-colleagues who betrayed her."},
    {"title": "Mrigratrishna", "language": "Kannada", "genre": "Drama", "price": "99",
     "image": "assets/images/movies/mrigi.avif", "desc": "An emotional story of love, destiny, and self-discovery.",
     "about": "The movie explores themes of fate, love, and self-realization through compelling storytelling."},
    {"title": "The Travellers", "language": "English", "genre": "Action", "price": "99",
     "image": "assets/images/movies/the travellers.avif", "desc": "Adventurers explore mysterious lands.",
     "about": "A group of explorers set out on a journey filled with danger, suspense, and discovery."},
    {"title": "Pets on Train", "language": "French", "genre": "Comedy", "price": "99",
     "image": "assets/images/movies/pets on train.avif", "desc": "A hilarious journey of pets traveling.",
     "about": "Follow the funny adventures of pets as they navigate train travel in France."},
    {"title": "Nuclear Now", "language": "English", "genre": "Sci-Fi", "price": "99",
     "image": "assets/images/movies/nuclear.avif", "desc": "A race against time to prevent a nuclear disaster.",
     "about": "Scientists must stop a catastrophic nuclear event from destroying the world."},
    {"title": "Lo Que Quisimos Ser", "language": "Spanish", "genre": "Drama", "price": "99",
     "image": "assets/images/movies/lo que.avif", "desc": "A touching tale of dreams and life choices.",
     "about": "The story follows characters navigating their ambitions, love, and the realities of life."},
    {"title": "Sir", "language": "Hindi", "genre": "Drama", "price": "99",
     "image": "assets/images/movies/sir.avif", "desc": "A heart-touching Hindi drama.",
     "about": "A story about love, struggle, and human relationships."}
]

   # ✅ map movie → youtube embed
STREAM_VIDEOS = {
    "John Wick": "https://www.youtube.com/embed/qEVUtrk8_B4",
    "Kill Bill": "https://www.youtube.com/embed/-SzkFgEqB6Y",
    "The Travellers": "https://www.youtube.com/embed/oD569HEsQL8",
    "Pets on Train": "https://www.youtube.com/embed/ZDME3FQUCPA",
    "Mrigratrishna": "https://www.youtube.com/embed/6HxrlxAnGh8",
    "Nuclear Now": "https://www.youtube.com/embed/wg20jTQLbT4",
    "Lo Que Quisimos Ser": "https://www.youtube.com/embed/SiCAZYc9HcQ",
    "Sir": "https://www.youtube.com/embed/VIDEO_ID_EMBED_ALLOWED"  # ❌ replace
}



# ----------------------- STREAM -----------------------
def stream(request):
    lang = request.GET.get('language')
    genre = request.GET.get('genre')

    filtered = STREAM_MOVIES
    if lang:
        filtered = [m for m in filtered if m['language'].lower() == lang.lower()]
    if genre:
        filtered = [m for m in filtered if m['genre'].lower() == genre.lower()]

    return render(request, "stream.html", {"stream_movies": filtered})


# ----------------------- STREAM DETAILS -----------------------
def stream_details(request):
    title = request.GET.get("movie")
    movie_obj = next((m for m in STREAM_MOVIES if m["title"] == title), None)
    if not movie_obj:
        return redirect("stream")

    return render(request, "stream_details.html", {"movie": movie_obj})


# ----------------------- STREAM PAYMENT -----------------------
@login_required
def stream_payment(request):
    movie = request.GET.get("movie")
    price = request.GET.get("price")

    if not movie or not price:
        return redirect("stream")

    total = int(price)

    # store in session for payment success
    request.session["stream_movie"] = movie
    request.session["stream_total"] = total

    return render(request, "stream_payment.html", {"movie": movie, "total": total})

# ----------------------- STREAM PAYMENT SUCCESS -----------------------
@login_required
def stream_payment_success(request):
    movie = request.session.get("stream_movie")
    total = request.session.get("stream_total")

    if not movie:
        messages.error(request, "No stream booking found.")
        return redirect("stream")  # fallback

    # Create booking record
    booking = Booking.objects.create(
        user=request.user,
        title=movie,
        booking_type="Stream",
        seats=1,
        price=total,
        date=timezone.now()
    )

    # Store session for watch access
    request.session["stream_paid_movie"] = movie
    request.session["stream_expires_at"] = (timezone.now() + timedelta(hours=48)).isoformat()

    # Clear old session keys
    for key in ["stream_movie", "stream_total"]:
        request.session.pop(key, None)

    # Redirect using slug in URL
    movie_slug = movie.replace(" ", "-")  # simple slug conversion
    return redirect("watch_stream", movie=movie_slug)

# ----------------------- STREAM WATCH -----------------------
@login_required
def stream_watch(request, movie):
    # Convert slug back to movie title
    movie_name = movie.replace("-", " ")
    expires = request.session.get("stream_expires_at")

    if not movie_name or not expires:
        messages.error(request, "You need to buy the stream first.")
        return redirect("stream")

    expires_dt = datetime.fromisoformat(expires)
    if timezone.is_naive(expires_dt):
        expires_dt = timezone.make_aware(expires_dt, timezone.get_current_timezone())

    if timezone.now() > expires_dt:
        del request.session["stream_paid_movie"]
        del request.session["stream_expires_at"]
        messages.error(request, "Your stream access has expired (48 hours).")
        return redirect("stream")

    youtube_link = STREAM_VIDEOS.get(movie_name)
    if not youtube_link:
        messages.error(request, "Video not found.")
        return redirect("stream")

    return redirect(youtube_link)


# -----------------------
# LIVE EVENTS DATA
# -----------------------

LIVE_EVENTS = [
    {
        "id": "telugu-standup-main",
        "name": "Telugu Standup @ Hyderabad",
        "category": "Comedy",
        "language": "Telugu",
        "venue": "The Street Comedy Club, Hyderabad",
        "date": "23 Jan 2026",
        "time": "07:00 PM",
        "duration": "1h 30m",
        "price": 499,
        "img": "assets/images/events/telugu standup.avif",
        "description": "Enjoy a fun-filled Telugu standup comedy night in Hyderabad.",
        "interested": 312
    },
    {
        "id": "inder-sahani",
        "name": "Aap Manoge Nahi ft. Inder Sahani",
        "category": "Comedy",
        "language": "Hindi",
        "venue": "TBD, Hyderabad",
        "date": "25 Jan 2026",
        "time": "08:00 PM",
        "duration": "1h 20m",
        "price": 499,
        "img": "assets/images/events/inder sahani.avif",
        "description": "Inder Sahani brings his viral standup show to Hyderabad.",
        "interested": 280
    },
    {
        "id": "cry-daddy",
        "name": "Cry Daddy ft. Anirban Dasgupta",
        "category": "Comedy",
        "language": "English / Hindi",
        "venue": "KLN Prasad Auditorium - FTCCI, Hyderabad",
        "date": "01 Feb 2026",
        "time": "07:00 PM",
        "duration": "1h 15m",
        "price": 799,
        "img": "assets/images/events/cry daddy.avif",
        "description": "Anirban Dasgupta's hit comedy show Cry Daddy live in Hyderabad.",
        "interested": 421
    },
    {
        "id": "red-flag-green-flag",
        "name": "Red Flag – Green Flag (Live Comedy Dating Show)",
        "category": "Comedy",
        "language": "Telugu / English",
        "venue": "KLN Prasad Auditorium – FTCCI, Hyderabad",
        "date": "07 Feb 2026",
        "time": "06:00 PM",
        "duration": "2h 30m",
        "price": 299,
        "img": "assets/images/events/red flag.avif",
        "description": "A hilarious live comedy dating show with audience interaction.",
        "interested": 820
    },
    {
    "id": "almost-may-be",
    "name": "Almost, May Be.. (Stand-up Comedy Show)",
    "category": "Comedy",
    "language": "English / Hindi",
    "venue": "The Habitat – Pune (and multiple cities)",
    "date": "21 Feb 2026 – 21 Mar 2026",
    "time": "7:30 PM",
    "duration": "1h 30m",
    "price": 399,
    "img": "assets/images/events/almost.avif",
    "description": "A stand-up comedy show by MRP featuring observational humor and personal life anecdotes.",
    "interested": 286
},
    #-------------------Theatre------------
    {
    "id": "kafan",
    "name": "KAFAN",
    "category": "Theatre",
    "language": "Hindi",
    "venue": "Lamakaan, Hyderabad",
    "date": "2026-02-01",
    "time": "08:00 PM",
    "duration": "45m",
    "price": 100,
    "img": "assets/images/events/kafan.avif",
    "description": "A powerful theatrical adaptation of Premchand’s classic story \"Kafan,\" exploring poverty, morality, and human nature.",
    "interested": 200
},
{
    "id": "jam-session-play",
    "name": "Jam Session by The 9 Club",
    "category": "Theatre",
    "language": "Telugu/English",
    "venue": "The 9 Club PaPaYa, Hyderabad",
    "date": "2026-02-15",
    "time": "05:00 PM",
    "duration": "2h",
    "price": 399,
    "img": "assets//images/plays/jamsession.avif",
    "description": "Live theatre combined with music and performance in this energetic jam session show.",
    "interested": 350
},
{
    "id": "aunty-moxie",
    "name": "Aunty Moxie is Delulu",
    "category": "Theatre",
    "language": "English",
    "venue": "Rangbhoomi Spaces & Events, Hyderabad",
    "date": "2026-03-01",
    "time": "06:00 PM",
    "duration": "1h 30m",
    "price": 400,
    "img": "assets/images/events/theatre/aunty_moxie.avif",
    "description": "A hilarious English theatre play about quirky characters and everyday life situations.",
    "interested": 420
},
{
    "id": "traasadi",
    "name": "Traasadi",
    "category": "Theatre",
    "language": "Hindi",
    "venue": "District 150, Hyderabad",
    "date": "2026-02-20",
    "time": "07:00 PM",
    "duration": "1h 45m",
    "price": 1299,
    "img": "assets/images/events/theatre/traasadi.avif",
    "description": "An engaging theatre experience with powerful storytelling and expressive performances.",
    "interested": 280
},

      # ---------------- Kids ----------------
    {
        "id": "kukdukoo-fest",
        "name": "Kukdukoo Fest Hyderabad",
        "category": "Kids",
        "language": "English/Hindi",
        "venue": "TBD, Hyderabad",
        "date": "15 Feb 2026",
        "time": "10:00 AM",
        "duration": "3h",
        "price": 299,
        "img": "assets/images/events/kukdukoo.avif",
        "description": "A fun-filled festival for kids with games and activities.",
        "interested": 120
    },
    {
        "id": "rambo-circus",
        "name": "Rambo Circus",
        "category": "Kids",
        "language": "English/Hindi",
        "venue": "Circus Grounds, Hyderabad",
        "date": "20 Feb 2026",
        "time": "11:00 AM",
        "duration": "2h",
        "price": 399,
        "img": "assets/images/events/rambo_circus.avif",
        "description": "Experience thrilling circus performances for kids.",
        "interested": 98
    },
    {
        "id": "gymnastics-kids",
        "name": "Kids Gymnastics",
        "category": "Kids",
        "language": "English/Hindi",
        "venue": "TBD, Hyderabad",
        "date": "22 Feb 2026",
        "time": "09:00 AM",
        "duration": "1h 30m",
        "price": 199,
        "img": "assets/images/events/gymnastics.avif",
        "description": "Gymnastics sessions and training for kids of all ages.",
        "interested": 75
    },
    # ---------------- Amusement ----------------
    {
        "id": "snow-kingdom",
        "name": "Snow Kingdom Hyderabad",
        "category": "Amusement",
        "language": "English/Hindi",
        "venue": "Snow Kingdom, Hyderabad",
        "date": "01 Mar 2026",
        "time": "10:00 AM",
        "duration": "4h",
        "price": 499,
        "img": "assets/images/events/snow_kingdom.avif",
        "description": "Experience snow and winter fun all year round!",
        "interested": 350
    },
    {
        "id": "ramoji-film-city",
        "name": "Ramoji Film City Hyderabad",
        "category": "Amusement",
        "language": "English/Hindi",
        "venue": "Ramoji Film City, Hyderabad",
        "date": "05 Mar 2026",
        "time": "09:00 AM",
        "duration": "6h",
        "price": 999,
        "img": "assets/images/events/ramoji.avif",
        "description": "Visit the famous Ramoji Film City with rides and shows.",
        "interested": 780
    },
    {
        "id": "wonderla-hyderabad",
        "name": "Wonderla Amusement Park",
        "category": "Amusement",
        "language": "English/Hindi",
        "venue": "Wonderla, Hyderabad",
        "date": "10 Mar 2026",
        "time": "10:00 AM",
        "duration": "5h",
        "price": 799,
        "img": "assets/images/events/wonderla.avif",
        "description": "Thrilling rides and water fun at Wonderla Hyderabad.",
        "interested": 560
    },
    {
        "id": "experium",
        "name": "Experium",
        "category": "Amusement",
        "language": "English/Hindi",
        "venue": "Experium, Hyderabad",
        "date": "12 Mar 2026",
        "time": "11:00 AM",
        "duration": "3h",
        "price": 299,
        "img": "assets/images/events/experium.avif",
        "description": "Interactive amusement experiences for families.",
        "interested": 120
    },
    {
        "id": "snow-world",
        "name": "Snow World Hyderabad",
        "category": "Amusement",
        "language": "English/Hindi",
        "venue": "Snow World, Hyderabad",
        "date": "15 Mar 2026",
        "time": "10:00 AM",
        "duration": "4h",
        "price": 499,
        "img": "assets/images/events/snow_world.avif",
        "description": "Snow-themed amusement park with rides and slides.",
        "interested": 250
    },
]
# --------------------------
# EVENTS HOME
# --------------------------
def events_home(request):
    return render(request, "events.html", {"events": LIVE_EVENTS})

# --------------------------
# CATEGORY FILTER
# --------------------------
def event_category(request, category):
    category = category.lower()
    if category == "theatre":
        return redirect("plays")  # redirect to plays page
    filtered = [e for e in LIVE_EVENTS if e["category"].lower() == category]
    return render(request, "event_category.html", {
        "events": filtered,
        "category": category.title()
    })

# --------------------------
# EVENT DETAILS
# --------------------------
def event_details(request, event_id):
    event = next((e for e in LIVE_EVENTS if e["id"] == event_id), None)
    if not event:
        return redirect("events")
    return render(request, "event_details.html", {"event": event})

# --------------------------
# EVENT PAYMENT
# --------------------------
def event_payment(request, event_id):
    event = next((e for e in LIVE_EVENTS if e["id"] == event_id), None)
    if not event:
        return redirect("events")

    qty = int(request.GET.get("tickets", 1))
    total = event["price"] * qty

    # Store in session for success page
    request.session["event_name"] = event["name"]
    request.session["event_tickets"] = qty
    request.session["event_price"] = total
    request.session["event_venue"] = event["venue"]

    return render(request, "event_payment.html", {
        "event": event,
        "qty": qty,
        "total": total
    })

# --------------------------
# EVENT PAYMENT SUCCESS
# --------------------------
@login_required
def event_payment_success(request):
    event_name = request.session.get("event_name")
    total = request.session.get("event_price")
    tickets = request.session.get("event_tickets")
    venue = request.session.get("event_venue")

    if not event_name:
        messages.error(request, "No event booking found.")
        return redirect("events")

    booking = Booking.objects.create(
        user=request.user,
        title=event_name,
        booking_type="Event",
        seats=tickets,
        price=total,
        date=timezone.now(),
        details=f"Venue: {venue}"
    )

    request.session["booking_id"] = booking.id
    for k in ["event_name", "event_price", "event_tickets", "event_venue"]:
        request.session.pop(k, None)

    return redirect("booking_success")


@login_required
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="ticket_{booking.id}.pdf"'

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, 800, "🎬 Booking Ticket")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 760, f"Type: {booking.booking_type}")
    pdf.drawString(50, 740, f"Title: {booking.title or booking.details}")
    pdf.drawString(50, 720, f"Seats: {booking.seats or 'N/A'}")
    pdf.drawString(50, 700, f"Show Time: {booking.show_time or 'N/A'}")
    pdf.drawString(50, 680, f"Amount Paid: ₹{booking.price}")
    pdf.drawString(50, 660, f"Date: {booking.date.strftime('%d %b %Y %I:%M %p')}")

    pdf.showPage()
    pdf.save()

    return response


    
# -----------------------
# STATIC PAGES
# -----------------------
def about(request):
    return render(request, "about.html")

def portfolio(request):
    return render(request, "portfolio.html", {
        "LIVE_EVENTS": LIVE_EVENTS,     
        "STREAM_MOVIES": STREAM_MOVIES  
    })

def contact(request):
    return render(request, "contact.html")

def services(request):
    return render(request, "services.html")
def profile(request):
    return render(request, "profile.html")
# ---------------- PLAYS DATA ----------------
PLAYS_LIST = [
    {"title": "Jam Session", "language": "Telugu/English", "genre": "Theatre", "price": 399, "venue": "The 9 Club PaPaYa", "date": "2026-02-15", "desc": "Enjoy live jam session performances.", "image": "assets/images/plays/jamsession.avif"},
    {"title": "Aunty Moxie is Delulu", "language": "English", "genre": "Theatre", "price": 400, "venue": "Rangbhoomi Spaces", "date": "2026-03-01", "desc": "A hilarious play about daily life.", "image": "assets/images/plays/auntymoxie.avif"},
    {"title": "Open Mic Comedy", "language": "English/Hindi", "genre": "Comedy", "price": 99, "venue": "The Comedy Theatre", "date": "2026-03-05", "desc": "Storytelling and comedy open mic.", "image": "assets/images/plays/openmic.avif"},
]

# ---------------- PLAYS PAGE ----------------
def plays(request):
    play_languages = sorted(list({p["language"] for p in PLAYS_LIST}))
    play_genres = sorted(list({p["genre"] for p in PLAYS_LIST}))
    return render(request, "plays.html", {
        "plays": PLAYS_LIST,
        "play_languages": play_languages,
        "play_genres": play_genres
    })

def play_payment(request):
    play = request.GET.get("play") or request.session.get("play_name")
    price = request.GET.get("price") or request.session.get("play_price")

    if not play or not price:
        return redirect("plays")

    # Store in session
    request.session["play_name"] = play
    request.session["play_price"] = int(price)

    # 🔥 HANDLE PAYMENT CONFIRM
    if request.method == "POST":
        return redirect("play_payment_success")

    return render(request, "play_payment.html", {
        "play": play,
        "price": price
    })

@login_required
def play_payment_success(request):
    play = request.session.get("play_name")
    price = request.session.get("play_price")
    venue = request.session.get("play_venue", "N/A")

    if not play:
        messages.error(request, "No play booking found.")
        return redirect("plays")

    booking = Booking.objects.create(
        user=request.user,
        booking_type="Play",
        details=f"{play} | Venue: {venue}",
        price=price,
        date=timezone.now(),
        title=play
    )

    request.session["booking_id"] = booking.id
    for k in ["play_name", "play_price", "play_venue"]:
        request.session.pop(k, None)

    return redirect("booking_success")


@login_required
def ticket(request):
    booking_id = request.session.get("booking_id")
    if not booking_id:
        return render(request, "error.html", {"message": "No booking found."})
    
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "ticket.html", {"booking": booking})


@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    return render(request, "my_bookings.html", {"bookings": bookings})
@login_required
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)
    booking.status = "Cancelled"
    booking.save()
    return redirect("my_bookings")
# -----------------------------
# SIGNUP WITH EMAIL OTP
# -----------------------------
# -----------------------------
# REUSABLE OTP SENDER
# -----------------------------
def send_otp(request, email, otp_type="signup"):
    """
    Sends OTP to the given email and stores it in session.

    otp_type: "signup" or "login"
    """
    otp = random.randint(100000, 999999)

    # Save OTP in session based on type
    session_key = f"{otp_type}_otp_data"
    request.session[session_key] = {
        "email": email,
        "otp": str(otp)
    }

    # Send OTP email
    subject = f"Your OTP for {otp_type.capitalize()}"
    message = f"Hello,\n\nYour OTP for {otp_type} is: {otp}\nIt is valid for 10 minutes.\n\nRegards,\nMovie Booking App"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        print(f"{otp_type.upper()} OTP sent to {email}: {otp}")  # for dev/debug
        messages.success(request, f"OTP sent to {email}")
        return True
    except Exception as e:
        print("Error sending OTP:", e)
        messages.error(request, "Failed to send OTP. Try again.")
        return False


# -----------------------------
# SIGNUP WITH EMAIL OTP
# -----------------------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup")

        # Send OTP using reusable function
        send_otp(request, email, otp_type="signup")

        # Save signup info in session
        request.session['signup_data'] = {
            "username": username,
            "email": email,
            "password": password
        }

        return redirect("otp_verify")

    return render(request, "signup.html")


def signup_otp_verify(request):
    if request.method == "POST":
        user_otp = request.POST.get("otp")
        otp_data = request.session.get("signup_otp_data")
        signup_data = request.session.get("signup_data")

        if not otp_data or not signup_data:
            messages.error(request, "Session expired. Try again.")
            return redirect("signup")

        if user_otp == otp_data["otp"]:
            # Create user
            user = User.objects.create_user(
                username=signup_data["username"],
                email=signup_data["email"],
                password=signup_data["password"]
            )
            login(request, user)
            # Clear sessions
            del request.session["signup_data"]
            del request.session["signup_otp_data"]
            return redirect("home")
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "otp_verify.html")


# -----------------------------
# USERNAME + PASSWORD LOGIN
# -----------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")


# -----------------------------
# EMAIL OTP LOGIN - Step 1: Request OTP
# -----------------------------
def otp_login_request(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not registered")
            return redirect("otp_login")

        # Send OTP using reusable function
        send_otp(request, email, otp_type="login")

        return redirect("otp_login_verify")

    return render(request, "otp_login.html")


# -----------------------------
# EMAIL OTP LOGIN - Step 2: Verify OTP
# -----------------------------
def otp_login_verify(request):
    if request.method == "POST":
        user_otp = request.POST.get("otp")
        otp_data = request.session.get("login_otp_data")

        if not otp_data:
            messages.error(request, "Session expired")
            return redirect("otp_login")

        if user_otp == otp_data["otp"]:
            user = User.objects.get(email=otp_data["email"])
            login(request, user)
            del request.session["login_otp_data"]
            return redirect("home")
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "otp_login_verify.html")


# -----------------------------
# LOGOUT
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect("home")