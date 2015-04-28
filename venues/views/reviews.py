from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
import json
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render, render_to_response
from django.views.decorators.http import require_POST, require_GET

from restaurant.utils import get_client_ip
from venues.forms import ReviewForm
from venues.models import Restaurant
from venues.models import Review

from django.contrib import messages

from venues.functions.get_ip import get_client_ip

@login_required
def review(request, rest_pk):
    '''
    rest_pk must be valid one for existing restaurant or
    ValueError will be raised on save() attempt in POST part.
    '''
    rest = get_object_or_404(Restaurant, id=rest_pk)

    context = {
        'venue_name': rest.name,
        'restaurant': rest
    }

    if request.method == u'GET':
        try:
            filterargs = {'venue_id': rest_pk, 'created_by': request.user}
            review = Review.objects.get(**filterargs)
            context['text'] = review.text
            context['rating'] = review.rating

        except ObjectDoesNotExist:
            pass

    if request.method == u'POST':

        filterargs = {'venue_id': rest_pk, 'user': request.user}
        try:
            review = Review.objects.get(**filterargs)
        except ObjectDoesNotExist:
            review = Review(user=request.user, content_object=rest)
        review.text = request.POST[u'review']
        review.rating = int(request.POST[u'rating'])
        review.save()
        context['text'] = review.text
        context['rating'] = review.rating
        context['is_saved'] = True
        rest.update_avg_rating()

    context.update(csrf(request))
    return render_to_response('reviews/review-form.html', context)


def show_all_reviews(request, rest_pk):
    reviews = Review.objects.filter(venue_id=rest_pk)
    data = serializers.serialize('json', reviews)
    data = json.loads(data)
    return HttpResponse(json.dumps({"response": {"total": len(data), "reviews": data}}),
                        content_type='application/json')


@login_required
@require_GET
def remove_review(request, review_pk):
    review = get_object_or_404(Review, id = review_pk)
    if not request.user.is_venue_moderator():
        if not (review.created_by == request.user):
            return redirect(reverse('django.contrib.auth.views.login') + "?next=%s" % request.path)
    Review.objects.get(pk=review_pk).delete()
    return redirect(request.META['HTTP_REFERER'])



@login_required
@require_POST
def add_review(request, rest_pk):
    _restaurant = Restaurant.objects.get(pk=rest_pk)
    related_object_type = ContentType.objects.get_for_model(_restaurant)

    ip=get_client_ip(request)

    review = Review(
        venue_id=_restaurant.pk,
        content_type=related_object_type,
        created_by=request.user,
        created_by_ip=ip
    )

    form = ReviewForm(request.POST, instance=review, request=request)
    if form.is_valid():
        form.save()
    _restaurant.update_avg_rating()
    _restaurant.update_review_counter()

    
    messages.add_message(request, messages.INFO, "Review is added!")
    return redirect(request.META['HTTP_REFERER'])


@login_required
def update_review(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    rest_pk = review.venue_id

    rest = get_object_or_404(Restaurant, id=rest_pk)

    context = {
        'restaurant': rest,
        'review': review,
        'ratings': xrange(1, 6),
    }

    if request.method == 'GET':
        if request.user.is_venue_moderator() or (review.created_by == request.user):
            context['form'] = ReviewForm(instance=review, request=request)
        else:
            return redirect(reverse('django.contrib.auth.views.login') + "?next=%s" % request.path)


    elif request.method == 'POST':
        if request.user.is_venue_moderator() or (review.created_by == request.user):
            form = ReviewForm(request.POST, instance=review, request=request)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, "Review is updated!")
                return render(request, 'reviews/update.html', context)
                # if rest.slug:
                #     return redirect(reverse('venues.views.venuess.restaurant_by_slug', args=[rest.slug]))
                # else:
                #     return redirect(reverse('venues.views.venuess.restaurant', args=[rest_pk]))
            else:
                context['form'] = form
        else:
            return redirect(reverse('django.contrib.auth.views.login') + "?next=%s" % request.path)
    
    return render(request, 'reviews/update.html', context)

