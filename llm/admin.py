from django.contrib import admin
from llm.models import Gemini2,ChatGPT
# Register your models here.

@admin.register(Gemini2)
class GeminiAdmin(admin.ModelAdmin):
    pass

@admin.register(ChatGPT)
class ChatGPTAdmin(admin.ModelAdmin):
    pass