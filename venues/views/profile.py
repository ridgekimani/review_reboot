from django.shortcuts import render
from venues.models.restaurant import Restaurant
from venues.models.venue import Venue

__author__ = 'm'

def index(request):
    restaurants = Restaurant.objects.filter(modified_by_id=request.user.pk)
    return render(request, "profile/index.html", {
        'restaurants': restaurants
    })