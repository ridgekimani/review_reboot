from account.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, render_to_response, get_object_or_404
from restaurant.utils import require_in_POST
from venues.models import Restaurant


def index(request):
    list = Restaurant.objects.order_by("approved", "name")
    paginator = Paginator(list, 10)
    page = request.GET.get("page")
    try:
        restaurants = paginator.page(page)
    except PageNotAnInteger:
        restaurants = paginator.page(1)
    except EmptyPage:
        restaurants = paginator.page(paginator.num_pages)

    context = {
        'restaurants': restaurants,
    }
    return render(request, "moderate/index.html", context)


@login_required
@user_passes_test(lambda u: u.is_venue_moderator)
def approve_restaurant(request, rest_pk):
    if request.method == "POST":
        restaurant = get_object_or_404(Restaurant, pk=rest_pk)
        restaurant.approved = request.POST['approved'] == u'true'
        restaurant.save()

        return HttpResponse()
    return HttpResponseBadRequest()

