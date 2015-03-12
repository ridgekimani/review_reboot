from django import forms
from django_countries.widgets import CountrySelectWidget
from venues.models import Restaurant, Comment, Note, Report

class RestaurantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RestaurantForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        extending base save method for allowing user tracking
        """
        if self.instance.pk is None:
            self.instance.created_by = self.user
        else:
            self.instance.modified_by = self.user
        super(RestaurantForm, self).save(commit)

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
