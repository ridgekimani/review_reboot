from account.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from venues.forms import VenueUserForm
from venues.models import Note
from venues.models import Review
from venues.models import VenueUser
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
        'reviews': modified_by_user_restaurants,
        'notes': modified_by_user_restaurants,
        'reports': modified_by_user_restaurants,
    })


@login_required
def myreviews(request):
    user_reviews = Review.objects.filter(created_by=request.user)

    return render(request, "profile/reviews.html", {
        'reviews': user_reviews
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


@login_required
def myprofile(request):
    user_reports = Report.objects.filter(created_by=request.user)
    user_notes = Note.objects.filter(created_by=request.user)
    user_reviews = Review.objects.filter(created_by=request.user)
    user_restaurants = Restaurant.objects.filter(created_by=request.user)

    return render(request, "profile/profile.html", {
        'reviews': user_reviews,
        'notes': user_notes,
        'restaurants': user_restaurants,
    })


class ProfileUpdateView(UpdateView):
    model = VenueUser
    form_class = VenueUserForm
    success_url = '/profile/'

    def get_initial(self):
        return {'username': self.request.user.username}

    def form_valid(self, form):
        user = self.request.user
        user.username = form.cleaned_data['username']
        user.save()
        return super(ProfileUpdateView, self).form_valid(form)

