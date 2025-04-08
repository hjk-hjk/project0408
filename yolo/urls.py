from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from yolo.views import yolo_helmet
# 경로 설정과 경로에 따른 함수 호출
urlpatterns = [
    path('yolo_helmet/', yolo_helmet , name='yolo_helmet'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)