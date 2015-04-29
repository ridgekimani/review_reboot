from django.core import serializers
from venues.models.note import Note

import json

def RestaurantSerializer(format, queryset, **options):

    MENU_TYPES = {0:"?",1:"Partially Halal",2: "Full Halal" }

    CHOICES = {None: "?",False: "No",True: "Yes"}
    obj_list = []
    for obj in queryset:
        obj.menu = MENU_TYPES[obj.menu]
        obj.porkFree = CHOICES[obj.porkFree]
        obj.muslimOwner = CHOICES[obj.muslimOwner]
        obj.alcoholFree = CHOICES[obj.alcoholFree]
        obj.catering = CHOICES[obj.catering]
        obj.delivery = CHOICES[obj.delivery]


        json_obj = serializers.serialize(format,(obj,),**options)
        obj_json = json.loads(json_obj)
        obj_json[0]['fields'].update({'note_count': len(Note.list_for_venue(obj))})

        obj_list.append(obj_json[0])

    json_return = json.dumps(obj_list)

    return json_return
