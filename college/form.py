from django.forms import forms
from college.models import Student

class CollegeForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['sno','sname','year','dept']