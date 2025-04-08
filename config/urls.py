from django.contrib import admin
from django.urls import path,include
from config.views import main , top, bottom

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('top/', top),
    path('bottom/', bottom),

    path('',include('burgers.urls')),
    path('',include('board.urls')),
    path('',include('college.urls')),
    path('',include('restfulapi.urls')),
    path('', include('llm.urls')),
    path('', include('yolo.urls')),
    path('', include('chatgpt.urls')),
]