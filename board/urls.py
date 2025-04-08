from django.urls import path
from board.views import board_list ,  board_edit
from board.views import board_form,board_delete

#경로 설정과 경로에 따른 (views에 있는)함수 호출
urlpatterns = [
    path('board_list/', board_list , name='board_list'),
    path('board_form/', board_form , name='board_form'),
    path('board_delete/<int:pk>/', board_delete , name='board_delete'),
    path('board_edit/<int:pk>/', board_edit , name='board_edit'),
]