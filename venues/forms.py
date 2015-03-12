from django import forms
from django_countries.widgets import CountrySelectWidget
from venues.models import Restaurant, Comment, Note, Report

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'cuisine', 'address', 'phone', 'categories', 'catering', 'delivery', 'alcoholFree',
                  'porkFree', 'muslimOwner', 'location', 'menu']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }


class AddressForm(forms.Form):
    address = forms.CharField(required=False)
    category = forms.CharField(required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['rating', 'text']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        exclude = ('modified_ip',)


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['type', 'note']
