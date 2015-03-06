from django import forms
from venues import models


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = ['name', 'cuisine', 'eatingOptions', 'address', 'yelp_url', 'foursquare_url', 'phone', 'categories',
                  'closed_reports_count']
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }


class AddressForm(forms.Form):
    address = forms.CharField(required=False)
    category = forms.CharField(required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['rating', 'text', 'user', 'content_type', 'venue_id']


class NoteForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ['user', 'content_type', 'venue_id', 'text']


class ReportForm(forms.ModelForm):
    class Meta:
        model = models.Report
        fields = ['report', 'note']