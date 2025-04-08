from django import forms

from yolo.models import Yolo


class YoloForm(forms.ModelForm):
    class Meta:
        model = Yolo
       # fields = ['name','year','dept']
        exclude = ['today']