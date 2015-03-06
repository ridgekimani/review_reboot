import json

from django.conf import settings
from restaurant.utils import get_client_ip
from venues.forms import CommentForm, NoteForm
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis import geos
from django.contrib.gis import measure
from django.views.decorators.http import require_GET, require_POST
from geopy.distance import distance as geopy_distance
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from social.apps.django_app.utils import psa
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from geopy.geocoders import Nominatim

from venues import models
from venues import forms


# from django.contrib.auth import logout
from venues.models import Restaurant, Comment, Note, Report, Category


def restaurants_lists(request):
    form = forms.AddressForm()
    restaurants = []
    latitude = ""
    longitude = ""
    if request.POST:
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
                    restaurants = models.Restaurant.objects.all
            else:
                geocoder = Nominatim()
                location = geocoder.geocode(address)
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
        context = {'all_restaurants': restaurants, 'form': form, 'longitude': longitude, 'latitude': latitude}
        return render(request, 'restaurants/restaurantlist.html', context)
    else:
        context = {'all_restaurants': restaurants, 'form': form, 'longitude': longitude, 'latitude': latitude}
        return render(request, 'restaurants/restaurants.html', context)


def get_category(request):
    if request.is_ajax():
        cat = request.GET['term']
        categories = models.Category.objects.filter(name__icontains=cat)[:20]
        results = []
        for category in categories:
            cat_json = {}
            cat_json['id'] = category.id
            cat_json['value'] = category.name
            results.append(cat_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


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
        return redirect(reverse('venues.views.restaurants_lists'))


@login_required
def comment(request, rest_pk):
    '''
    rest_pk must be valid one for existing restaurant or 
    ValueError will be raised on save() attempt in POST part. 
    '''
    rest = get_object_or_404(Restaurant, id=rest_pk)

    context = {
        'venue_name': rest.name
    }

    if request.method == u'GET':
        try:
            filterargs = {'venue_id': rest_pk, 'user': request.user}
            comment = models.Comment.objects.get(**filterargs)
            context['text'] = comment.text
            context['rating'] = comment.rating

        except ObjectDoesNotExist:
            pass

    if request.method == u'POST':

        filterargs = {'venue_id': rest_pk, 'user': request.user}
        try:
            comment = models.Comment.objects.get(**filterargs)
        except ObjectDoesNotExist:
            comment = models.Comment(user=request.user, content_object=rest)
        comment.text = request.POST[u'comment']
        comment.rating = int(request.POST[u'rating'])
        comment.save()
        context['text'] = comment.text
        context['rating'] = comment.rating
        context['is_saved'] = True
        rest.update_avg_rating()

    context.update(csrf(request))
    return render_to_response('restaurants/../restaurant/templates/comments/comment-form.html', context)


def show_all_comments(request, rest_pk):
    comments = models.Comment.objects.filter(venue_id=rest_pk)
    data = serializers.serialize('json', comments)
    data = json.loads(data)
    return HttpResponse(json.dumps({"response": {"total": len(data), "comments": data}}),
                        content_type='application/json')


#
# @login_required
# def update_note(request, note_pk):
# note = Note.objects.get(pk=note_pk)
# if request.method == 'GET':
#


def show_all_tips(request, rest_pk):
    tips = models.Note.objects.filter(venue_id=rest_pk)
    data = serializers.serialize('json', tips)
    data = json.loads(data)
    return HttpResponse(json.dumps({"response": {"total": len(data), "tips": data}}), content_type='application/json')


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
                return redirect(reverse('venues.views.restaurant_by_slug', args=[_restaurant.slug]))
            else:
                return redirect(reverse('venues.views.restaurant', args=[rest_pk]))
        context['form'] = form
    else:
        context['form'] = forms.RestaurantForm(instance=_restaurant)

    return render(request, 'restaurants/update.html', context)


def report_restaurant(request, rest_pk):
    rest = models.Restaurant.objects.get(id=rest_pk)
    related_object_type = ContentType.objects.get_for_model(rest)

    context = {
        'venue_name': rest.name
    }

    if request.method == 'GET':
        context['form'] = forms.ReportForm()
        return render(request, 'reports/report.html', context)
    elif request.method == 'POST':
        data = request.POST.copy()

        report = Report(
            user=request.user if request.user.is_authenticated() else None,
            content_type=related_object_type,
            modified_ip=get_client_ip(request),
            venue_id=rest_pk,
        )

        form = forms.ReportForm(request.POST, instance=report)

        context['form'] = form

        if form.is_valid():
            form.save()

            if form.cleaned_data['report'] == u'closed':
                rest.update_close_state()

            if rest.slug:
                return redirect(reverse('venues.views.restaurant_by_slug', args=[rest.slug]))
            else:
                return redirect(reverse('venues.views.restaurant', args=[rest_pk]))

        return render(request, 'reports/report.html', context)


@login_required
def moderate_reports(request):
    if request.user.username not in settings.ALLOWED_TO_MODERATE:
        return HttpResponse(status=500)

    reports = models.Report.objects.all()
    paginator = Paginator(
        sorted(reports, key=lambda r: r.created_on, reverse=True),
        10
    )
    page = request.GET.get('page')
    try:
        context = {'reports': paginator.page(page)}
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        context = {'reports': paginator.page(1)}
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        context = {'reports': paginator.page(paginator.num_pages)}

    context.update(csrf(request))
    return render(request, 'reports/moderate_reports.html', context)


def moderate_report(request, pk):
    if request.method == 'POST':
        report = models.Report.objects.get(id=pk)
        if 'moderator_flag' in request.POST:
            report.moderator_flag = True
        if 'moderator_note' in request.POST:
            report.moderator_note = request.POST['moderator_note']
        report.moderator = request.user
        report.save()
        return redirect(
            '/moderate-reports/?page={n}'.format(
                n=request.POST['page_num']
            )
        )


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


@login_required
@require_GET
def remove_comment(request, comment_pk):
    Comment.objects.get(pk=comment_pk).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required
@require_POST
def add_comment(request, rest_pk):
    _restaurant = Restaurant.objects.get(pk=rest_pk)
    related_object_type = ContentType.objects.get_for_model(_restaurant)

    comment = Comment(
        user=request.user,
        venue_id=_restaurant.pk,
        content_type=related_object_type,
        modified_ip=get_client_ip(request),
    )

    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def update_comment(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    rest_pk = comment.venue_id

    rest = get_object_or_404(Restaurant, id=rest_pk)

    context = {
        'restaurant': rest,
        'comment': comment,
        'ratings': xrange(1, 6),
    }

    if request.method == 'GET':
        context['form'] = CommentForm(instance=comment)
    elif request.method == 'POST':
        comment.modified_ip = get_client_ip(request)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            if rest.slug:
                return redirect(reverse('venues.views.restaurant_by_slug', args=[rest.slug]))
            else:
                return redirect(reverse('venues.views.restaurant', args=[rest_pk]))
        else:
            context['form'] = form

    return render(request, 'comments/update.html', context)


@login_required
@require_GET
def remove_note(request, note_pk):
    Note.objects.get(pk=note_pk).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required
@require_POST
def add_note(request, rest_pk):
    _restaurant = Restaurant.objects.get(pk=rest_pk)
    related_object_type = ContentType.objects.get_for_model(_restaurant)

    note = Note(
        user=request.user,
        venue_id=_restaurant.pk,
        content_type=related_object_type,
        modified_ip=get_client_ip(request)
    )

    form = NoteForm(request.POST,instance=note)
    if form.is_valid():
        form.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def update_note(request, note_pk):
    note = Note.objects.get(pk=note_pk)
    rest_pk = note.venue_id

    rest = get_object_or_404(Restaurant, id=rest_pk)

    context = {
        'restaurant': rest,
        'note': note,
    }

    if request.method == 'GET':
        context['form'] = NoteForm(instance=note)
    elif request.method == 'POST':
        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            note.modified_ip = get_client_ip(request)
            form.save()
            if rest.slug:
                return redirect(reverse('venues.views.restaurant_by_slug', args=[rest.slug]))
            else:
                return redirect(reverse('venues.views.restaurant', args=[rest_pk]))
        else:
            context['form'] = form

    return render(request, 'notes/update.html', context)


@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.GET.get('access_token')
    user = request.backend.do_auth(request.GET.get('access_token'))
    if user:
        login(request, user)
        return HttpResponse(json.dumps({"success": True}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"success": False}), content_type='application/json')

