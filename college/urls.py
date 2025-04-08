from django.urls import path
from college.views import student_list,student_enrol,student_course
from college.views import s_c_e,subquery1,subquery2,student_form
urlpatterns = [
    path('student_list/', student_list , name='student_list'),
    path('student_enrol/', student_enrol , name='student_enrol'),
    path('student_course/', student_course , name='student_course'),
    path('s_c_e/', s_c_e , name='s_c_e'),
    path('subquery1/', subquery1 , name='subquery1'),
    path('subquery2/', subquery2 , name='subquery2'),
    path('student_form/', student_form , name='student_form'),

]