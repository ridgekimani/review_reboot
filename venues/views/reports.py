from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.context_processors import csrf
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from restaurant.utils import get_client_ip
from venues import forms
from venues.models import Restaurant
from venues.models.report import Report


def report_restaurant(request, rest_pk):
    rest = Restaurant.objects.get(id=rest_pk)
    related_object_type = ContentType.objects.get_for_model(rest)

    context = {
        'venue_name': rest.name
    }

    if request.method == 'GET':
        context['form'] = forms.ReportForm(request=request)
        return render(request, 'reports/report.html', context)
    elif request.method == 'POST':
        data = request.POST.copy()

        report = Report(
            content_type=related_object_type,
            venue_id=rest_pk,
        )

        form = forms.ReportForm(request.POST, instance=report, request=request)

        context['form'] = form

        if form.is_valid():
            form.save()

            # if form.cleaned_data['tipe'] == ':
            #     rest.update_close_state()

            if rest.slug:
                return redirect(reverse('venues.views.venuess.restaurant_by_slug', args=[rest.slug]))
            else:
                return redirect(reverse('venues.views.venuess.restaurant', args=[rest_pk]))

        return render(request, 'reports/report.html', context)


@login_required
def moderate_reports(request):
    reports = Report.objects.all()
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
        report = Report.objects.get(id=pk)
        if 'moderator_flag' in request.POST:
            report.moderator_flag = True
        if 'moderator_note' in request.POST:
            report.moderator_note = request.POST['moderator_note']
        report.save()
        return redirect(
            '/moderate-reports/?page={n}'.format(
                n=request.POST['page_num']
            )
        )