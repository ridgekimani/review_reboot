import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, Http404
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.gis import geos
from django.contrib.gis import measure
from django.views.decorators.http import require_GET
from geopy.distance import distance as geopy_distance
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from geopy.geocoders import Nominatim
from tastypie.http import HttpBadRequest

from restaurant.utils import get_client_ip

from venues import models
from venues import forms
from venues.forms import RestaurantForm
from venues.models import Restaurant, Comment, Note, Report, Category


def get_masjids(longitude, latitude, categories):
    '''
    Returns objects at given point that satisfy set of categories,
    or all of them if categories is empty.
    input:
        str longitude
        str latitude
        list categories
    output:
        list of dicts
    '''
    currentPoint = geos.GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
    distance_m = 15000
    list_of_cats = []
    for c in categories:
        list_of_cats.append(models.Category.objects.get(name=c))
    if list_of_cats:
        masjids = models.Masjid.gis.filter(
            location__distance_lte=(currentPoint, distance_m),
            categories__in=list_of_cats
        )
    else:
        masjids = models.Masjid.gis.filter(location__distance_lte=(currentPoint, distance_m))

    # String based JSON
    data = serializers.serialize('json', masjids)
    # Actual JSON object to be edited
    data = json.loads(data)

    # if venue has multiple categories and some of them
    # are in list_of_cats than venue will appear in data that some times
    # so we will uniqify venues in data
    if len(list_of_cats) > 1:
        data = {v['pk']: v for v in data}.values()

    for masjid in data:
        d = geopy_distance(currentPoint, masjid['fields']['location']).kilometers
        masjid['fields']['distance'] = round(d, 1)

        # Fancy splitting on POINT(lon, lat)
        lng = masjid['fields']['location'].split()[1][1:]
        lat = masjid['fields']['location'].split()[2][:-1]

        del masjid['fields']['location']
        masjid['fields']['lng'] = lng
        masjid['fields']['lat'] = lat

        # Replace category ids with names
        cat_names = []
        for cat_id in masjid['fields']['categories']:
            cat = models.Category.objects.get(id=cat_id)
            cat_names.append(cat.name)
        masjid['fields']['categories'] = cat_names

    return data


def restaurants_lists(request):
    form = forms.AddressForm()
    restaurants = []
    latitude = ""
    longitude = ""
    if request.POST:
        page = request.POST.get('page')
        form = forms.AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            category = form.cleaned_data['category']

            list_of_cats = []
            if category:
                try:
                    list_of_cats.append(models.Category.objects.get(name__icontains=category))
                except (MultipleObjectsReturned):
                    length = models.Category.objects.filter(name__icontains=category).__len__()
                    for l in range(length):
                        list_of_cats.append(models.Category.objects.filter(name__icontains=category)[l])
                except (ObjectDoesNotExist):
                    pass
            if not address:
                if list_of_cats:
                    restaurants = models.Restaurant.objects.filter(categories__in=list_of_cats)
                else:
                    restaurants = models.Restaurant.objects.all()
                try:
                    longitude, latitude = restaurants[0].location
                except IndexError:
                    pass
            else:
                geocoder = Nominatim()
                try:
                    location = geocoder.geocode(address)
                except Exception as e:
                    print e
                    location = ""

                if location:
                    latitude = location.latitude
                    longitude = location.longitude
                    currentPoint = geos.GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
                    distance_m = {'km': 15}
                    if list_of_cats:
                        restaurants = models.Restaurant.gis.filter(
                            location__distance_lte=(currentPoint, measure.D(**distance_m)),
                            categories__in=list_of_cats
                        ).distance(currentPoint)
                    else:
                        restaurants = models.Restaurant.gis.filter(
                            location__distance_lte=(currentPoint, measure.D(**distance_m))).distance(currentPoint)
    else:
        page = request.GET.get('page')
        restaurants = Restaurant.objects.all()

    paginator = Paginator(restaurants, 5)
    page = request.GET.get("page")
    try:
        restaurants = paginator.page(page)
    except PageNotAnInteger:
        restaurants = paginator.page(1)
    except EmptyPage:
        restaurants = paginator.page(paginator.num_pages)

    context = {'all_restaurants': restaurants, 'form': form, 'longitude': longitude, 'latitude': latitude}
    return render(request, 'restaurants/restaurants.html', context)
    # else:
    #     context = {'all_restaurants': restaurants, 'form': form, 'longitude': longitude, 'latitude': latitude}
    #     return render(request, 'restaurants/restaurants.html', context)


def get_restaurants(longitude, latitude, categories):
    '''
    Returns objects at given point that satisfy set of categories,
    or all of them if categories is empty.
    input:
        str longitude
        str latitude
        list categories
    output:
        list of dicts
    '''
    currentPoint = geos.GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
    distance_m = 15000
    list_of_cats = []
    for c in categories:
        list_of_cats.append(models.Category.objects.get(name=c))
    if list_of_cats:
        restaurants = models.Restaurant.gis.filter(
            location__distance_lte=(currentPoint, distance_m),
            categories__in=list_of_cats,
            is_closed=False
        )
    else:
        restaurants = models.Restaurant.gis.filter(
            location__distance_lte=(currentPoint, distance_m),
            is_closed=False
        )

    # seems that this thing doesn't actually order objects by distance
    # btw at this step there is no distance property in objects or rows in table
    # restaurants = restaurants.distance(currentPoint).order_by('distance')

    # String based JSON
    data = serializers.serialize('json', restaurants)
    # Actual JSON object to be edited
    data = json.loads(data)

    # if venue has multiple categories and some of them
    # are in list_of_cats than venue will appear in data that some times
    # so we will uniqify venues in data
    if len(list_of_cats) > 1:
        data = {v['pk']: v for v in data}.values()

    for restaurant in data:
        d = geopy_distance(currentPoint, restaurant['fields']['location']).kilometers
        restaurant['fields']['distance'] = round(d, 1)

        # Fancy splitting on POINT(lon, lat)
        lng = restaurant['fields']['location'].split()[1][1:]
        lat = restaurant['fields']['location'].split()[2][:-1]

        del restaurant['fields']['location']
        restaurant['fields']['lng'] = lng
        restaurant['fields']['lat'] = lat

        # Replace category ids with names
        cat_names = []
        for cat_id in restaurant['fields']['categories']:
            cat = models.Category.objects.get(id=cat_id)
            cat_names.append(cat.name)
        restaurant['fields']['categories'] = cat_names

    return data


@require_GET
def closest(request):
    if 'lat' in request.GET and 'lon' in request.GET:

        lat = float(request.GET['lat'])
        lon = float(request.GET['lon'])
        if 'category' in request.GET:
            categories = request.GET['category'].split('+')
        else:
            categories = []

        response_message = ''

        if request.GET.has_key('masjids'):
            venues = get_masjids(lon, lat, categories)
            if not venues:
                venues = get_masjids(lon, lat, categories=[])
                response_message = "No venues for this categories, here are some other ones you might like"
        else:
            venues = get_restaurants(lon, lat, categories)
            if not venues:
                venues = get_restaurants(lon, lat, categories=[])
                response_message = "No venues for this categories, here are some other ones you might like"

        return HttpResponse(
            json.dumps({
                "response": {
                    "total": len(venues),
                    "venues": sorted(venues, key=lambda venue: venue['fields']['distance']),
                    "message": response_message
                }
            }),
            content_type='application/json'
        )
    else:
        return redirect(reverse('venues.views.venuess.restaurants_lists'))


# @login_required
# def log_out(request):
# logout(request)
# return render(request, "comment.html")

def restaurant(request, rest_pk):
    _restaurant = Restaurant.objects.get(pk=rest_pk)
    return render(request, 'restaurants/item.html', {
        'restaurant': _restaurant,
        'comments': Comment.list_for_venue(_restaurant).order_by('-modified_on'),
        'notes': Note.list_for_venue(_restaurant).order_by('-modified_on'),
        'reports': Report.list_for_venue(_restaurant),
    })


@user_passes_test(lambda u: u.is_venue_moderator)
def remove_restaurant(request, rest_pk):
    if request.method == "POST":
        rest = get_object_or_404(Restaurant, pk=rest_pk)
        rest.delete()
        return HttpResponse()
    return HttpResponseBadRequest()


@login_required
def add_restaurant(request):
    if request.method == "GET":
        form = RestaurantForm()
        return render(request, "restaurants/new.html", {
            "form": form,
            "categories": Category.objects.all()
        })
    elif request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            new_restaurant = form.save()
            return redirect(reverse('venues.views.venuess.restaurant_by_slug', args=[new_restaurant.slug]))
        elif not request.is_ajax():
            return render(request, "restaurants/new.html", {
                "form": form,
                "categories": Category.objects.all()
            })
        return HttpBadRequest(form.errors())
    return HttpBadRequest()


@login_required
def update_restaurant(request, rest_pk):
    _restaurant = Restaurant.objects.get(pk=rest_pk)
    context = {
        'restaurant': _restaurant,
        'comments': Comment.list_for_venue(_restaurant),
        'notes': Note.list_for_venue(_restaurant),
        'reports': Report.list_for_venue(_restaurant),
    }

    if request.method == 'POST':
        rest_data = request.POST.copy()
        rest_data['modified_ip'] = get_client_ip(request)
        form = forms.RestaurantForm(rest_data, instance=_restaurant)  # A form bound to the POST data
        if form.is_valid():
            form.save()
            # context['is_saved'] = True
            if _restaurant.slug:
                return redirect(reverse('venues.views.venuess.restaurant_by_slug', args=[_restaurant.slug]))
            else:
                return redirect(reverse('venues.views.venuess.restaurant', args=[rest_pk]))
        context['form'] = form
    else:
        context['form'] = forms.RestaurantForm(instance=_restaurant)

    return render(request, 'restaurants/update.html', context)


def restaurant_by_slug(request, slug):
    '''
    find restaurant instance by slug and return it profile page
    or raise 404 if nothing finds
    :param request:
    :param slug:
    :return:
    '''
    r = Restaurant.objects.filter(slug=slug).first()
    if not r:
        raise Http404()
    else:
        return restaurant(request, r.pk)

