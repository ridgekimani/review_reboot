from account.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, render_to_response, get_object_or_404
from venues.models import Restaurant
from venues.models.comment import Comment


@user_passes_test(lambda u: u.is_venue_moderator())
def index(request):

    # approved items paginator
    list = Restaurant.objects.order_by("approved", "name")
    paginatorApproved = Paginator(list, 10)
    page = request.GET.get("page")
    try:
        restaurants = paginatorApproved.page(page)
    except PageNotAnInteger:
        restaurants = paginatorApproved.page(1)
    except EmptyPage:
        restaurants = paginatorApproved.page(paginatorApproved.num_pages)

    # updated restaurants
    list = Restaurant.objects.order_by("-modified_on")
    paginatorApproved = Paginator(list, 10)
    page = request.GET.get("pageUpdated")
    try:
        recently_update_restaurants = paginatorApproved.page(page)
    except PageNotAnInteger:
        recently_update_restaurants = paginatorApproved.page(1)
    except EmptyPage:
        recently_update_restaurants = paginatorApproved.page(paginatorApproved.num_pages)

    # added reviews
    list = Comment.objects.order_by("-modified_on")
    paginatorApproved = Paginator(list, 10)
    page = request.GET.get("pageReview")
    try:
        recently_added_reviews = paginatorApproved.page(page)
    except PageNotAnInteger:
        recently_added_reviews = paginatorApproved.page(1)
    except EmptyPage:
        recently_added_reviews = paginatorApproved.page(paginatorApproved.num_pages)

    context = {
        'restaurants': restaurants,
        'recently_update_restaurants': recently_update_restaurants,
        'recently_added_reviews': recently_added_reviews,
    }
    return render(request, "moderate/index.html", context)


@login_required
@user_passes_test(lambda u: u.is_venue_moderator())
def approve_restaurant(request, rest_pk):
    if request.method == "POST":
        restaurant = get_object_or_404(Restaurant, pk=rest_pk)
        restaurant.approved = request.POST['approved'] == u'true'
        restaurant.save()

        return HttpResponse()
    return HttpResponseBadRequest()

