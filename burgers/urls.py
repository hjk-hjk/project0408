from django.urls import path
from burgers.views import burger_list ,  burger_search
from burgers.views import burger_form,burger_delete,burger_edit
urlpatterns = [

    path('burger_list/', burger_list , name='burger_list'),
    path('burger_search/', burger_search, name='burger_search' ),
    path('burger_form/', burger_form , name='burger_form'),
    path('burger_delete/<int:pk>/', burger_delete , name='burger_delete'),
    path('burger_edit/<int:pk>/', burger_edit , name='burger_edit'),
]