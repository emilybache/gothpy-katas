from django import forms

from models import WebUser

class WebUserForm(forms.ModelForm):
    class Meta:
        model = WebUser

class SearchUserForm(forms.Form):
    search = forms.CharField(max_length=50)