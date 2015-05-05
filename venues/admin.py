from django.contrib.auth.models import User
from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.admin import UserAdmin
from venues.models import Restaurant, Masjid, Sect

from venues.models import Review
from venues.models.cuisine import Cuisine
from venues.models.note import Note
from venues.models.report import Report
from venues.models.venue_user import VenueUser

from venues.forms import ProfileForm

class VenueUserInline(admin.StackedInline):
    model = VenueUser
    can_delete = False
    verbose_name_plural = 'venue user'


class UserAdmin(UserAdmin):
    inlines = (VenueUserInline, )
    list_display = UserAdmin.list_display + ('is_superuser', 'venue_moderator',)

    def venue_moderator(self, obj):
        user = VenueUser.objects.filter(user=obj).first()
        if user:
            return user.venue_moderator
        else:
            return obj.is_superuser
    venue_moderator.boolean = True
    # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# VENUES

class MasjidAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'id', 'phone', 'twitter_url', 'facebook_url')


class RestaurantAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'id', 'catering', 'delivery')
    search_fields = ['name']

#
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('venue_name', 'rating', 'short_text', 'created_by')
#     fields = (('venue_name', 'created_by'), 'rating', 'text')
#     readonly_fields = ('venue_name',)
#
#
# class NoteAdmin(admin.ModelAdmin):
#     list_display = ('venue_name', 'text', 'created_by')
#     fields = (('venue_name', 'created_by'), 'text')
#     readonly_fields = ('venue_name',)


class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

class AdminProfileForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'sex')
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
    )
    list_filter = ('sex',)
    raw_id_fields = ('user',)
    exclude = ('user',)
    form = AdminProfileForm

    def first_name(self, instance):
        return instance.user.first_name

    def last_name(self, instance):
        return instance.user.last_name


admin.site.register(VenueUser, ProfileAdmin)

# Register your models here.
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Masjid, MasjidAdmin)
# admin.site.register(Comment, CommentAdmin)
admin.site.register(Cuisine, CuisineAdmin)
# admin.site.register(Note, NoteAdmin)
admin.site.register(Report, admin.ModelAdmin)
admin.site.register(Sect)