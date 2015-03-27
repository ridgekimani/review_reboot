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
from django.contrib.auth.models import User

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


__author__ = 'm'



@login_required
def approvedrestaurants(request):
    user_restaurants = Restaurant.objects.filter(approved=False).exclude(is_suspended=True)
    suspended = Restaurant.objects.filter(is_suspended=True)
    paginatorApproved = Paginator(user_restaurants, 10)
    page = request.GET.get("page")
    try:
        restaurants = paginatorApproved.page(page)
    except PageNotAnInteger:
        restaurants = paginatorApproved.page(1)
    except EmptyPage:
        restaurants = paginatorApproved.page(paginatorApproved.num_pages)


    paginatorApproved = Paginator(list(suspended), 10)
    page = request.GET.get("pageSuspended")
    try:
        suspended = paginatorApproved.page(page)
    except PageNotAnInteger:
        suspended = paginatorApproved.page(1)
    except EmptyPage:
        suspended = paginatorApproved.page(paginatorApproved.num_pages)

    return render(request, "profile/approved.html", {
        'user_restaurants': user_restaurants,
        'restaurants': restaurants,
        'suspended':suspended
    })


@login_required
def myreviews(request):
    user_reviews = Review.objects.filter(created_by=request.user)

    return render(request, "profile/reviews.html", {
        'reviews': user_reviews
    })


@login_required
def myprofile(request):
    user_reports = Report.objects.filter(created_by=request.user)
    user_notes = Note.objects.filter(created_by=request.user).order_by('-created_on')
    user_reviews = Review.objects.filter(created_by=request.user).order_by('-created_on')
    user_restaurants = Restaurant.objects.filter(created_by=request.user)
    list = Restaurant.objects.filter(modified_by=request.user)


    paginatorApproved = Paginator(list, 10)
    page = request.GET.get("pageUpdated")
    try:
        user_updates = paginatorApproved.page(page)
    except PageNotAnInteger:
        user_updates = paginatorApproved.page(1)
    except EmptyPage:
        user_updates = paginatorApproved.page(paginatorApproved.num_pages)

    for rest in user_updates.object_list:
        items = rest.history_link.filter(id=rest.id).order_by("-history_date")
        changed_fields = []
        if items.count() > 1:
            previous = items[1]
            if previous:
                for field in rest._meta.get_all_field_names():
                    if field not in ['cuisines', 'modified_by', 'created_by', 'modified_by_id', 'created_by_id',
                                     'modified_on', 'slug'] and getattr(rest, field) != getattr(previous, field):
                        changed_fields.append(field)
        else:
            changed_fields.append("created")
        rest.changed_fields = changed_fields


    return render(request, "profile/profile.html", {
        'reviews': user_reviews,
        'notes': user_notes,
        'restaurants': user_restaurants,
        'updates': user_updates
    })

@login_required
def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    user_reports = Report.objects.filter(created_by=user)
    user_notes = Note.objects.filter(created_by=user).order_by('-created_on')
    user_reviews = Review.objects.filter(created_by=user).order_by('-created_on')
    list = Restaurant.objects.filter(modified_by=user)


    paginatorApproved = Paginator(list, 10)
    page = request.GET.get("pageUpdated")
    try:
        user_updates = paginatorApproved.page(page)
    except PageNotAnInteger:
        user_updates = paginatorApproved.page(1)
    except EmptyPage:
        user_updates = paginatorApproved.page(paginatorApproved.num_pages)

    for rest in user_updates.object_list:
        items = rest.history_link.filter(id=rest.id).order_by("-history_date")
        changed_fields = []
        if items.count() > 1:
            previous = items[1]
            if previous:
                for field in rest._meta.get_all_field_names():
                    if field not in ['cuisines', 'modified_by', 'created_by', 'modified_by_id', 'created_by_id',
                                     'modified_on', 'slug'] and getattr(rest, field) != getattr(previous, field):
                        changed_fields.append(field)
        else:
            changed_fields.append("created")
        rest.changed_fields = changed_fields


    return render(request, "profile/profile.html", {
        'reviews': user_reviews,
        'notes': user_notes,
        'updates': user_updates,
        'user': user
    })



@login_required
def updated_restaurants(request):
    # updated restaurants
    list = Restaurant.objects.order_by("-modified_on")
    paginatorApproved = Paginator(list, 10)
    page = request.GET.get("pageUpdated")
    try:
        recently_update_restaurants = paginatorApproved.page(page)
    except PageNotAnInteger:
        recently_update_restaurants = paginatorApproved.page(1)
    except EmptyPage:
        recently_update_restaurants = paginatorApproved.page(paginatorApproved.num_pages)

    # checking for restaurant changed fields
    # which can be accessed via changed_fields property
    for rest in recently_update_restaurants.object_list:
        items = rest.history_link.filter(id=rest.id).order_by("-history_date")
        changed_fields = []
        if items.count() > 1:
            previous = items[1]
            if previous:
                for field in rest._meta.get_all_field_names():
                    if field not in ['cuisines', 'modified_by', 'created_by', 'modified_by_id', 'created_by_id',
                                     'modified_on', 'slug'] and getattr(rest, field) != getattr(previous, field):
                        changed_fields.append(field)
        else:
            changed_fields.append("created")
        rest.changed_fields = changed_fields
    context = {
        'recently_update_restaurants': recently_update_restaurants
    }
    return render(request, "profile/updated.html", context)


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

