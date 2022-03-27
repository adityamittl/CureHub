from django import forms
from PIL import Image

class diagnosis_form(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=100)
    report = forms.ImageField()
    remark = forms.CharField(widget=forms.Textarea)
    price = forms.IntegerField()

