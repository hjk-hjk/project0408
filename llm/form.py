from django.forms import forms

from llm.models import Gemini2,ChatGPT


class GeminiForm(forms.ModelForm):
    class Meta:
        model = Gemini2
       # fields = ['sno','name','year','dept']
        exclude = ['today']

class ChatGPTForm(forms.ModelForm):
    class Meta:
        model = ChatGPT
       # fields = ['sno','name','year','dept']
        exclude = ['today']