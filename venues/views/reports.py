from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.core.context_processors import csrf
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404

from restaurant.utils import get_client_ip
from venues import forms
from venues.models import Restaurant, Masjid
from venues.models.report import Report, ReportType
from django.contrib import messages


@login_required
def report_restaurant(request, rest_pk):
    rest = Restaurant.objects.get(id=rest_pk)
    related_object_type = ContentType.objects.get_for_model(rest)

    context = {
        'venue_name': rest.name
    }

    if request.method == 'GET':
        form = forms.ReportForm(request=request)

        form.fields['report_type'].queryset = ReportType.objects.filter(venue_type = related_object_type)
        context['form'] = form
        return render(request, 'reports/report.html', context)
    elif request.method == 'POST':
        data = request.POST.copy()

        report = Report(
            content_type=related_object_type,
            venue_id=rest_pk,
        )

        form = forms.ReportForm(request.POST, instance=report, request=request)
        form.fields['report_type'].queryset = ReportType.objects.filter(venue_type = related_object_type)
        context['form'] = form

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Report Submitted")
            # if form.cleaned_data['tipe'] == ':
            # rest.update_close_state()

            if rest.slug:
                return redirect(reverse('venues.views.venuess.restaurant_by_slug', args=[rest.slug]))
            else:
                return redirect(reverse('venues.views.venuess.restaurant', args=[rest_pk]))


        return render(request, 'reports/report.html', context)

@login_required
@user_passes_test(lambda u: u.is_venue_moderator())
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


@login_required
@user_passes_test(lambda u: u.is_venue_moderator())
def moderate_report(request, pk):
    if request.method == 'POST':
        report = get_object_or_404(Report, id=pk)
        if 'resolved' in request.POST:
            report.resolved = request.POST['resolved'].lower() == 'true'
        if 'moderator_note' in request.POST:
            report.moderator_note = request.POST['moderator_note']
        report.save()
        #postfix = "?page=%d" % request.POST['page_num'] if 'page_num' in request.POST else ''
        return redirect(reverse("venues.views.reports.moderate_reports")) #+ postfix)



@login_required
def report_masjid(request, masjid_pk):
    masjid = Masjid.objects.get(id=masjid_pk)
    related_object_type = ContentType.objects.get_for_model(masjid)

    context = {
        'venue_name': masjid.name
    }

    if request.method == 'GET':
        form = forms.ReportForm(request=request)

        form.fields['report_type'].queryset = ReportType.objects.filter(venue_type = related_object_type)
        context['form'] = form
        return render(request, 'reports/report.html', context)
    elif request.method == 'POST':
        data = request.POST.copy()

        report = Report(
            content_type=related_object_type,
            venue_id=masjid_pk,
        )

        form = forms.ReportForm(request.POST, instance=report, request=request)
        form.fields['report_type'].queryset = ReportType.objects.filter(venue_type = related_object_type)
        context['form'] = form

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Report Submitted")

            if masjid.slug:
                return redirect(reverse('venues.views.venuess.masjid_by_slug', args=[masjid.slug]))
            else:
                return redirect(reverse('venues.views.venuess.masjid', args=[masjid_pk]))


        return render(request, 'reports/report.html', context)
