from django.core import serializers


def RestaurantSerializer(format, queryset, **options):

    MENU_TYPES = {0:"?",1:"Partially Halal",2: "Full Halal" }

    CHOICES = {None: "?",False: "No",True: "Yes"}

    for obj in queryset:
        obj.menu = MENU_TYPES[obj.menu]
        obj.porkFree = CHOICES[obj.porkFree]
        obj.catering = CHOICES[obj.catering]
        obj.muslimOwner = CHOICES[obj.muslimOwner]

    return serializers.serialize(format,queryset, **options)