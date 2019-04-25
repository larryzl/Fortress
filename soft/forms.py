from django import forms
from django.forms import widgets
from django.forms import fields
from soft.models import Soft


class SoftForm(forms.ModelForm):

    class Meta:
        model = Soft
        fields = ('name','version','describe','soft_icon')
