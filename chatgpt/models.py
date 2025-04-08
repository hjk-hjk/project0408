from django.db import models

class ChatGPT(models.Model):
    objects = None
    name = models.CharField(max_length=20)
    aiexplain = models.TextField()
    file = models.FileField(upload_to='chatgpt/')
    today = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name}_{self.today}"