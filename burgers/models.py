from django.db import models

# Create your models here.
class  Burger(models.Model):
    objects = None
    name = models.CharField(max_length=20) # 이름
    price = models.IntegerField(default = 0)  # 가격
    calories  = models.IntegerField(default = 0)  # 칼로리

    def __str__(self):
        return self.name