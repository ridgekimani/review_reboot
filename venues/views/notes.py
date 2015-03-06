from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.serializers import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST, require_GET
from restaurant.utils import get_client_ip
from venues.forms import NoteForm
from venues.models import Restaurant, Note



def show_all_notes(request, rest_pk):
    notes = Note.objects.filter(venue_id=rest_pk)
    data = serializers.serialize('json', notes)
    data = json.loads(data)
    return HttpResponse(json.dumps({"response": {"total": len(data), "tips": data}}), content_type='application/json')


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

    form = NoteForm(request.POST, instance=note)
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
                return redirect(reverse('venues.views.venuess.restaurant_by_slug', args=[rest.slug]))
            else:
                return redirect(reverse('venues.views.venuess.restaurant', args=[rest_pk]))
        else:
            context['form'] = form

    return render(request, 'notes/update.html', context)
