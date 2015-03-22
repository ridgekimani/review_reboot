from django.http import HttpResponse, Http404
import json
from django.views.decorators.http import require_POST, require_GET
from venues.jsonAPI.masjid import get_masjids
from django.contrib.gis.geos import Point
from venues.models import Masjid, Restaurant

from django.core import serializers

from geopy.distance import distance as geopy_distance
from venues.models.cuisine import Cuisine



@require_GET
def closest(request):
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
        venues = __get_restaurants(request, lon, lat, categories)
        if not venues:
            venues = __get_restaurants(request, lon, lat, categories=[])
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


def __get_restaurants(request, longitude, latitude, categories, limit=20):
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
    currentPoint = Point(float(longitude), float(latitude))  # geos.GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
    distance_m = 15000
    list_of_cats = []
    for c in categories:
        list_of_cats.append(Cuisine.objects.get(name=c))
    if list_of_cats:
        restaurants = Restaurant.gis.filter(
            location__distance_lte=(currentPoint, distance_m),
            cuisines__in=list_of_cats,
            is_closed=False
        )
    else:
        restaurants = Restaurant.gis.filter(
            location__distance_lte=(currentPoint, distance_m),
            is_closed=False
        )

    if hasattr(request.user, 'is_venue_moderator') and request.user.is_venue_moderator():
        pass
    else:
        restaurants = restaurants.filter(approved=True)

    # seems that this thing doesn't actually order objects by distance
    # btw at this step there is no distance property in objects or rows in table
    # restaurants = restaurants.distance(currentPoint).order_by('distance')
    restaurants = restaurants[:limit]
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

        # Replace cuisine ids with names
        cat_names = []
        for cat_id in restaurant['fields']['cuisines']:
            cat = Cuisine.objects.get(id=cat_id)
            cat_names.append(cat.name)
        restaurant['fields']['cuisines'] = cat_names

    return data