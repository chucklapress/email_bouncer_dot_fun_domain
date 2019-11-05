from django import forms
from django.forms import ModelForm
from email_parser.models import dmarc_check

class EmailForm(forms.Form):

    address = forms.EmailField(required=True)
    return_from = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    the_dmarc_check = forms.CharField(widget=forms.Textarea)

class dmarc_checkForm(ModelForm):
    class Meta:
        model = dmarc_check
        fields = "__all__"
