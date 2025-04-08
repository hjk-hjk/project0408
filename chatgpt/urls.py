from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from chatgpt.views import chatgpt_form
# 경로 설정과 경로에 따른 함수 호출
urlpatterns = [
    path('chatgpt_form/', chatgpt_form , name='chatgpt_form'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
