from venues.models import VenueUser


def social_profile_link(backend, user, is_new, request, response, *args, **kwargs):
    user = VenueUser.objects.get_or_create(user=user)[0]
    if backend.name == 'facebook':
        user.social_profile = 'https://www.facebook.com/{}'.format(response['id'])
    user.save()
