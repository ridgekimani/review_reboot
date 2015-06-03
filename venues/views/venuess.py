import json
from django.contrib.gis.geos import Point

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponse, Http404
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.gis import geos
from django.contrib.gis import measure
from django.views.decorators.http import require_GET
from geopy.distance import distance as geopy_distance
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from geopy.geocoders import Nominatim, GoogleV3
from tastypie.http import HttpBadRequest

from restaurant.utils import get_client_ip
from venues import forms
from venues.forms import RestaurantForm, MasjidForm
from venues.models import Masjid, Restaurant
from venues.models import Review
from venues.models.cuisine import Cuisine
from venues.models.note import Note
from venues.models.report import Report

from django.contrib import messages 

from venues.jsonAPI.restaurants import __get_restaurants,closest
from venues.jsonAPI.masjid import get_masjids



GOOGLE_KEY = 'AIzaSyAJ7o-jjLVWcaAXaW_fe0hnTsQeyhxsBBQ'

def search_view(request):
    if 'lat' in request.GET and 'lon' in request.GET:
        #return closest(request)
        return closest(request)
    else:
        return HttpResponse("qwe")

def index(request):

    if request.user.is_authenticated() and not request.user.venueuser.location:
        return redirect('profile-form', pk=request.user.venueuser.pk)


    if 'lat' in request.GET and 'lon' in request.GET:
        return closest(request)

    form = forms.AddressForm()
    restaurants = []
    latitude = ""
    longitude = ""
    address = ""
    name = ""
    if request.POST:
        page = request.POST.get('page')
        form = forms.AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            name = form.cleaned_data['name']
            if not address:
                restaurants = Restaurant.objects.filter(approved=True, is_suspended=False,name__icontains=name)
                try:
                    longitude, latitude = restaurants[0].location
                except IndexError:
                    pass
            else:
                geocoder = GoogleV3(api_key=GOOGLE_KEY)
                try:
                    location = geocoder.geocode(address)
                except Exception as e:
                    print e
                    location = ""

                if location:
                    latitude = location.latitude
                    longitude = location.longitude
                    currentPoint = geos.GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
                    distance_m = {'km': 30}
                    restaurants = Restaurant.gis.filter(approved=True,
                            location__distance_lte=(currentPoint, measure.D(**distance_m)),
                            name__icontains=name).distance(currentPoint).order_by('distance')
    else:
        page = request.GET.get('page')
        restaurants = Restaurant.objects.filter(approved=True, is_suspended=False)

    #if hasattr(request.user, 'is_venue_moderator') and request.user.is_venue_moderator():
    #    pass
    #else:
    #    restaurants = Restaurant.objects.filter(approved=True, is_suspended=False)

    paginator = Paginator(restaurants, 20)
    page = request.GET.get("page")
    try:
        restaurants = paginator.page(page)
    except PageNotAnInteger:
        restaurants = paginator.page(1)
    except EmptyPage:
        restaurants = paginator.page(paginator.num_pages)
    
    context = {'all_restaurants': restaurants, 'form': form, 'longitude': longitude, 'latitude': latitude, 'address':address, 'name':name}
    return render(request, 'restaurants/restaurants.html', context)
    # else:
    # context = {'all_restaurants': restaurants, 'form': form, 'longitude': longitude, 'latitude': latitude}
    # return render(request, 'restaurants/restaurants.html', context)


def restaurant(request, rest_pk):
  
    _restaurant = get_object_or_404(Restaurant, pk=rest_pk)
    note_form = forms.NoteForm()
    if not _restaurant.approved and \
            not (hasattr(request.user, 'is_venue_moderator') and request.user.is_venue_moderator()):
        return render(request, 'restaurants/submitted.html',{
                "restaurant_slug":_restaurant.slug
                })

    if request.user.is_authenticated():
        reveiw_by_user = Review.objects.filter(venue_id = rest_pk, created_by = request.user)
        note_by_user=Note.objects.filter(venue_id = rest_pk, created_by=request.user)

    else:
        reveiw_by_user = None
        note_by_user = None
    
    
    reviews = Review.objects.filter(venue_id = _restaurant.pk).order_by('-created_on')
    notes = Note.objects.filter(venue_id = _restaurant.pk).order_by('-created_on')
    return render(request, 'restaurants/restaurantProfile.html', {
        'restaurant': _restaurant,
        'reviews': Review.list_for_venue(_restaurant).order_by('-modified_on'),
        'notes': Note.list_for_venue(_restaurant).order_by('-modified_on'),
        'reports': Report.list_for_venue(_restaurant),
        'note_form' : note_form,
        'reviews' : reviews,
        'notes' : notes,
        'reveiw_by_user' : reveiw_by_user ,
        'note_by_user' : note_by_user
    })

@login_required
@require_GET
def add_review_view(request,rest_pk):
    _restaurant = get_object_or_404(Restaurant, pk=rest_pk)
    if not _restaurant.approved and \
            not (hasattr(request.user, 'is_venue_moderator') and request.user.is_venue_moderator()):
        raise Http404

    reveiw_by_user = Review.objects.filter(venue_id = rest_pk, created_by = request.user)
    return render(request, 'restaurants/restaurant_writereview.html', {
        'restaurant': _restaurant,
        'reveiw_by_user' : reveiw_by_user,
    })

@login_required
@require_GET
def add_note_view(request,rest_pk):
    _restaurant = get_object_or_404(Restaurant, pk=rest_pk)
    if not _restaurant.approved and \
            not (hasattr(request.user, 'is_venue_moderator') and request.user.is_venue_moderator()):
        raise Http404

    return render(request, 'restaurants/restaurant_addnote.html', {
        'restaurant': _restaurant,
    })



@login_required
def add_restaurant(request):
    if request.method == "GET":
        form = RestaurantForm(request=request)
        return render(request, "restaurants/addRestaurant.html", {
            "form": form,
            "categories": Cuisine.objects.all()
        })
    elif request.method == "POST":
        rest_data = request.POST.copy()
        #rest_data['cuisines'] = [int(rest_data['cuisines']), ]
        form = RestaurantForm(rest_data, request=request)
        if form.is_valid():
            new_restaurant = form.save()
            return render(request, 'restaurants/submitted.html',{
                "restaurant_slug":new_restaurant.slug
                })
            #return redirect(reverse('venues.views.venuess.restaurant_by_slug', args=[new_restaurant.slug]))
        elif not request.is_ajax():
            return render(request, "restaurants/addRestaurant.html", {
                "form": form,
                "categories": Cuisine.objects.all()
            })
        return HttpBadRequest(form.errors())
    return HttpBadRequest()


@login_required
def update_restaurant(request, rest_pk):
    _restaurant = get_object_or_404(Restaurant, pk=rest_pk)

    #if not request.user.is_venue_moderator():
    #    if not (_restaurant.created_by == request.user and not _restaurant.approved):
    #        return redirect(reverse('django.contrib.auth.views.login') + "?next=%s" % request.path)

    context = {
        'restaurant': _restaurant,
        'reviews': Review.list_for_venue(_restaurant),
        'notes': Note.list_for_venue(_restaurant),
        'reports': Report.list_for_venue(_restaurant),
    }

    if request.method == 'POST':
        rest_data = request.POST.copy()
        #rest_data['cuisines'] = [int(rest_data['cuisines']), ]
        # rest_data['cuisines'] = list([int(i) for i in rest_data['cuisines']])
        form = forms.RestaurantForm(rest_data, instance=_restaurant, request=request)  # A form bound to the POST data
        if form.is_valid():
            form.save()
            # context['is_saved'] = True
            if _restaurant.slug:
                return redirect(reverse('venues.views.venuess.restaurant_by_slug', args=[_restaurant.slug]))
            else:
                return redirect(reverse('venues.views.venuess.restaurant', args=[rest_pk]))
        context['form'] = form
    else:
        context['form'] = forms.RestaurantForm(instance=_restaurant, request=request)

    return render(request, 'restaurants/update.html', context)


def restaurant_by_slug(request, slug):
    '''
    find restaurant instance by slug and return it profile page
    or raise 404 if nothing finds
    :param request:
    :param slug:
    :return:
    '''
    r = get_object_or_404(Restaurant, slug=slug)
    return restaurant(request, r.pk)


def all_reviews_view(request, rest_pk):
    rest = get_object_or_404(Restaurant, pk=rest_pk)

    reviews = Review.objects.filter(venue_id=rest_pk)

    return render(request, 'reviews/all_reviews.html',{
        'reviews':reviews,
        'restaurant':rest
        })

def all_notes_view(request, rest_pk):
    rest = get_object_or_404(Restaurant, pk=rest_pk)

    notes = Note.objects.filter(venue_id=rest_pk)

    return render(request, 'notes/all_notes.html',{
        'notes':notes,
        'restaurant':rest
        })




@login_required
def add_masjid(request):
    if request.method == "GET":
        form = MasjidForm(request=request)
        return render(request, "masjids/addMasjid.html", {
            "form": form,
        })
    elif request.method == "POST":
        rest_data = request.POST.copy()
        #rest_data['cuisines'] = [int(rest_data['cuisines']), ]
        form = MasjidForm(rest_data, request=request)
        if form.is_valid():
            new_masjid = form.save()
            return render(request, 'masjids/submitted.html',{
                "masjid_slug":new_masjid.slug
                })
            #return redirect(reverse('venues.views.venuess.restaurant_by_slug', args=[new_restaurant.slug]))
        elif not request.is_ajax():
            return render(request, "masjids/addMasjid.html", {
                "form": form,
            })
        return HttpBadRequest(form.errors())
    return HttpBadRequest()


def masjid_by_slug(request, slug):

    m = get_object_or_404(Masjid, slug=slug)
    return masjid(request, m.pk)



def masjid(request, masjid_pk):

    _masjid = get_object_or_404(Masjid, pk=masjid_pk)
    if not _masjid.approved and \
            not (hasattr(request.user, 'is_venue_moderator') and request.user.is_venue_moderator()):
        return render(request, 'masjids/submitted.html',{
                "masjid_slug":_masjid.slug
                })


    return render(request, 'masjids/masjidProfile.html', {
        'masjid': _masjid,
        'reports': Report.list_for_venue(_masjid),
    })



@login_required
def update_masjid(request, masjid_pk):
    _masjid = get_object_or_404(Masjid, pk=masjid_pk)

    context = {
        'masjid': _masjid,
        'reports': Report.list_for_venue(_masjid),
    }

    if request.method == 'POST':
        masjid_data = request.POST.copy()
        form = forms.MasjidForm(masjid_data, instance=_masjid, request=request)  # A form bound to the POST data
        if form.is_valid():
            form.save()
            if _masjid.slug:
                return redirect(reverse('venues.views.venuess.masjid_by_slug', args=[_masjid.slug]))
            else:
                return redirect(reverse('venues.views.venuess.masjid', args=[masjid_pk]))
        context['form'] = form
    else:
        context['form'] = forms.MasjidForm(instance=_masjid, request=request)

    return render(request, 'masjids/update.html', context)

