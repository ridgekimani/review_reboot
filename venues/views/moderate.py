from django.shortcuts import render
from venues.models import Restaurant


def index(request):
    context = {
        'restaurants': Restaurant.objects.filter(approved=False),
        'approved': Restaurant.objects.filter(approved=True),
    }
    return render(request, "moderate/index.html", context)
