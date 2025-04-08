from  django  import  forms
from  chatgpt.models import  ChatGPT

class  ChatGPTForm(forms.ModelForm):
    class  Meta:
        model = ChatGPT
        #fields = ['title','name','content']
        exclude = ['today']