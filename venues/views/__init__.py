import json

from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import login
from social.apps.django_app.utils import psa

from venues import models


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

