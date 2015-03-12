from django.shortcuts import render
from venues.models import Note
from venues.models.comment import Comment
from venues.models.report import Report
from venues.models.restaurant import Restaurant
from venues.models.venue import Venue

__author__ = 'm'

def index(request):
    user_restaurants = Restaurant.objects.filter(created_by=request.user)
    modified_by_user_restaurants = Restaurant.objects.filter(modified_by=request.user)\
        .exclude(pk__in=user_restaurants)

    user_comments = Comment.objects.filter(created_by=request.user)
    user_notes = Note.objects.filter(created_by=request.user)
    user_reports = Report.objects.filter(created_by=request.user)

    return render(request, "profile/index.html", {
        'user_restaurants': user_restaurants,
        'modified_by_user_restaurants': modified_by_user_restaurants,
        'comments': modified_by_user_restaurants,
        'notes': modified_by_user_restaurants,
        'reports': modified_by_user_restaurants,
    })