from django.urls import path
from restfulapi.views import restful_json,restful_json_sql
from restfulapi.views import restful_txt_sql,restful_xml_sql
from restfulapi.views import request_json_sql,request_xml_sql
urlpatterns = [
    path('restful_json/', restful_json , name='restful_json'),
    path('restful_json_sql/', restful_json_sql , name='restful_json_sql'),
    path('restful_txt_sql/', restful_txt_sql , name='restful_txt_sql'),
    path('restful_xml_sql/', restful_xml_sql , name='restful_xml_sql'),
    path('request_json_sql/', request_json_sql , name='request_json_sql'),
    path('request_xml_sql/', request_xml_sql , name='request_xml_sql'),
   ]
