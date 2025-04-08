from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from llm.views import gemini_txt, gemini_img,gemini_delete,alibaba_api
from llm.views import chatgpt_api,chatgpt_api_img,chatgpt_delete
# 경로 설정과 경로에 따른 함수 호출
urlpatterns = [
    path('gemini_txt/', gemini_txt , name='gemini_txt'),
    path('gemini_img/', gemini_img, name='gemini_img'),
    path('gemini_delete/<int:pk>/', gemini_delete , name='gemini_delete'),
    path('alibaba_api/', alibaba_api , name='alibaba_api'),
    path('chatgpt_api/', chatgpt_api , name='chatgpt_api'),
    path('chatgpt_api_img/', chatgpt_api_img , name='chatgpt_api_img'),
    path('chatgpt_delete/', chatgpt_delete , name='chatgpt_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
