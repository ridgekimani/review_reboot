from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin
from venues import models

class MasjidAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'id', 'phone', 'twitter_url','facebook_url')

class RestaurantAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'id', 'phone', 'yelp_id', 'yelp_url','foursquare_id','foursquare_url', 'avg_rating')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'rating', 'short_text', 'user')
    fields = (('venue_name', 'user'), 'rating', 'text')
    readonly_fields = ('venue_name',)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'text', 'user')
    fields = (('venue_name', 'user'), 'text')
    readonly_fields = ('venue_name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

# Register your models here.
admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.Masjid, MasjidAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Note, NoteAdmin)
admin.site.register(models.Report, admin.ModelAdmin)