from django import forms
from board.models import Board

#board_form.html 의 form 태그 안에서 사용
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        #fields = ['title','name','content','today']
        exclude = ['today']