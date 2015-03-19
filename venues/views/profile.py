from account.decorators import login_required
from django.shortcuts import render
from venues.models import Note
from venues.models.comment import Comment
from venues.models.report import Report
from venues.models.restaurant import Restaurant
from venues.models.venue import Venue

__author__ = 'm'


@login_required
def myrestaurants(request):
    user_restaurants = Restaurant.objects.filter(created_by=request.user)
    modified_by_user_restaurants = Restaurant.objects.filter(modified_by=request.user) \
        .exclude(pk__in=user_restaurants)

    return render(request, "profile/restaurants.html", {
        'user_restaurants': user_restaurants,
        'modified_by_user_restaurants': modified_by_user_restaurants,
        'comments': modified_by_user_restaurants,
        'notes': modified_by_user_restaurants,
        'reports': modified_by_user_restaurants,
    })


@login_required
def mycomments(request):
    user_comments = Comment.objects.filter(created_by=request.user)

    return render(request, "profile/comments.html", {
        'comments': user_comments
    })

@login_required
def mynotes(request):
    user_notes = Note.objects.filter(created_by=request.user)

    return render(request, "profile/notes.html", {
        'notes': user_notes
    })

@login_required
def myreports(request):
    user_reports = Report.objects.filter(created_by=request.user)

    return render(request, "profile/reports.html", {
        'reports': user_reports
    })
