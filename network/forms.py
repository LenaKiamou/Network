from django.forms import ModelForm
from django import forms
from .models import *

class NewPost(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "textarea","placeholder": "Write your post here"}))
    class Meta:
        model = Post
        fields = ['description']
