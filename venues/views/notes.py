from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST, require_GET
from restaurant.utils import get_client_ip
from venues.forms import NoteForm
from venues.models import Restaurant
from venues.models.note import Note

from django.contrib import messages

from venues.functions.get_ip import get_client_ip

def show_all_notes(request, rest_pk):
    notes = Note.objects.filter(venue_id=rest_pk)
    data = serializers.serialize('json', notes)
    data = json.loads(data)
    return HttpResponse(json.dumps({"response": {"total": len(data), "tips": data}}), content_type='application/json')


@require_GET
@login_required
def remove_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    if request.user.is_venue_moderator() or note.created_by==request.user:
        note.delete()
    else:
        return redirect(reverse("account_login"))

    if request.is_ajax():
        return HttpResponse()
    else:
        if 'HTTP_REFERER' in request.META:
            return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect(reverse("venues.views.venuess.index"))


@login_required
@require_POST
def add_note(request, rest_pk):
    _restaurant = get_object_or_404(Restaurant, pk=rest_pk)
    if not _restaurant.approved and not request.user.is_venue_moderator():
        return redirect(reverse("account_login"))

    related_object_type = ContentType.objects.get_for_model(_restaurant)
    ip = get_client_ip(request)
    note = Note(
        venue_id=_restaurant.pk,
        content_type=related_object_type,
        created_by_ip = ip
    )

    form = NoteForm(request.POST, instance=note, request=request)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, "Note is added!")

    if request.is_ajax():
        return HttpResponse()
    else:
        if 'HTTP_REFERER' in request.META:
            return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect(reverse("venues.views.venuess.index"))


@login_required
def update_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    rest_pk = note.venue_id

    rest = get_object_or_404(Restaurant, id=rest_pk)

    context = {
        'restaurant': rest,
        'note': note,
    }

    if not rest.approved and not request.user.is_venue_moderator():
        return redirect(reverse('account_login'))

    if request.method == 'GET':
        context['form'] = NoteForm(instance=note, request=request)
    elif request.method == 'POST':
        form = NoteForm(request.POST, instance=note, request=request)

        if form.is_valid():
            form.save()
            if rest.slug:
                return redirect(reverse('venues.views.venuess.restaurant_by_slug', args=[rest.slug]))
            else:
                return redirect(reverse('venues.views.venuess.restaurant', args=[rest_pk]))
        else:
            context['form'] = form

    return render(request, 'notes/update.html', context)
