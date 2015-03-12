from django import forms
from django_countries.widgets import CountrySelectWidget
from restaurant.utils import get_client_ip
from venues.models import Restaurant, Comment, Note, Report


class CommonForm(forms.ModelForm):
    """
    this is CommonForm for CommonModel,
    make sure to provide request argument to make it work
    """
    def __init__(self, *args, **kwargs):
        """
        make sure to provide request argument when contruction form
        """
        self.request = kwargs.pop('request', None)
        super(CommonForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        extending base save method for allowing request tracking
        """
        if self.request:
            if self.instance.pk is None:
                self.instance.created_by = self.request.user
            else:
                self.instance.modified_by = self.request.user

            self.instance.modified_ip = get_client_ip(self.request)

        super(CommonForm, self).save(commit)


class RestaurantForm(CommonForm):
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


class CommentForm(CommonForm):
    class Meta:
        model = Comment
        fields = ['rating', 'text']


class NoteForm(CommonForm):
    class Meta:
        model = Note
        fields = ['text']


class ReportForm(CommonForm):
    class Meta:
        model = Report
        fields = ['type', 'note']
