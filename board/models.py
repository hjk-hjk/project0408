from django.db import models

#테이블과 마이그래이션 하기위한 클래스 생성
# Create your models here.
class Board(models.Model):
    objects=None
    title = models.CharField(max_length=30)
    name = models.CharField(max_length=10)
    content = models.TextField()
    today = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title