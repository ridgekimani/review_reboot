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
from venues.forms import CommentForm
from venues.models import Restaurant
from venues.models.comment import Comment


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
            comment = Comment.objects.get(**filterargs)
            context['text'] = comment.text
            context['rating'] = comment.rating

        except ObjectDoesNotExist:
            pass

    if request.method == u'POST':

        filterargs = {'venue_id': rest_pk, 'user': request.user}
        try:
            comment = Comment.objects.get(**filterargs)
        except ObjectDoesNotExist:
            comment = Comment(user=request.user, content_object=rest)
        comment.text = request.POST[u'comment']
        comment.rating = int(request.POST[u'rating'])
        comment.save()
        context['text'] = comment.text
        context['rating'] = comment.rating
        context['is_saved'] = True
        rest.update_avg_rating()

    context.update(csrf(request))
    return render_to_response('comments/comment-form.html', context)


def show_all_comments(request, rest_pk):
    comments = Comment.objects.filter(venue_id=rest_pk)
    data = serializers.serialize('json', comments)
    data = json.loads(data)
    return HttpResponse(json.dumps({"response": {"total": len(data), "comments": data}}),
                        content_type='application/json')


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
        venue_id=_restaurant.pk,
        content_type=related_object_type,
    )

    form = CommentForm(request.POST, instance=comment, request=request)
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
        context['form'] = CommentForm(instance=comment, request=request)
    elif request.method == 'POST':
        form = CommentForm(request.POST, instance=comment, request=request)
        if form.is_valid():
            form.save()
            if rest.slug:
                return redirect(reverse('venues.views.venuess.restaurant_by_slug', args=[rest.slug]))
            else:
                return redirect(reverse('venues.views.venuess.restaurant', args=[rest_pk]))
        else:
            context['form'] = form

    return render(request, 'comments/update.html', context)

