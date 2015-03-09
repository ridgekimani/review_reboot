from django import forms
from venues import models


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = ['name', 'cuisine', 'address', 'phone', 'categories', 'catering', 'delivery', 'alcoholFree',
                  'porkFree', 'muslimOwner']
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }


class AddressForm(forms.Form):
    address = forms.CharField(required=False)
    category = forms.CharField(required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['rating', 'text']


class NoteForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ['text']
        exclude = ('modified_ip',)


class ReportForm(forms.ModelForm):
    class Meta:
        model = models.Report
        fields = ['report', 'note']
