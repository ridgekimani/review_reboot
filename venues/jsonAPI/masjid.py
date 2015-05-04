from django.contrib.gis import geos
from venues.models import Masjid, Restaurant
import json
from venues.models.cuisine import Cuisine
from django.core import serializers



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
        list_of_cats.append(Cuisine.objects.get(name=c))
    if list_of_cats:
        masjids = Masjid.gis.filter(
            location__distance_lte=(currentPoint, distance_m),
            categories__in=list_of_cats
        )
    else:
        masjids = Masjid.gis.filter(location__distance_lte=(currentPoint, distance_m))

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
        for cat_id in masjid['fields']['cuisines']:
            cat = Cuisine.objects.get(id=cat_id)
            cat_names.append(cat.name)
        masjid['fields']['cuisines'] = cat_names

    return data