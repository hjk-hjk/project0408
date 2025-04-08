from django.db import models

class  Student(models.Model):
    objects = None
    sno = models.CharField(max_length=3, primary_key=True ) # 학번
    sname = models.CharField(max_length=15)  # 이름
    year  = models.IntegerField(default = 1) # 학년
    dept  = models.CharField(max_length=20)  # 학과
    def __str__(self):
        return self.sname


class  Course(models.Model):
    objects = None
    cno = models.CharField(max_length=4, primary_key=True ) # 학번
    cname = models.CharField(max_length=20)  # 이름
    credit   = models.IntegerField(default = 1) # 학년
    dept  = models.CharField(max_length=20)  # 학과
    prname  = models.CharField(max_length=20)  # 학과
    def __str__(self):
        return self.cname


class Enrol(models.Model):
    sno = models.ForeignKey(Student, on_delete=models.CASCADE)  # 학번에 대해 외래 키
    cno = models.ForeignKey(Course, on_delete=models.CASCADE)  # 과목코드에 대해 외래 키
    grade = models.CharField(max_length=1)  # 평점
    midterm = models.IntegerField()  # 중간성적
    gimal = models.IntegerField()  # 기말성적

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sno', 'cno'], name='restful_U_S_C')  # sno와 cno 조합 유니크 설정
        ]

    def __str__(self):
        return f"{self.sno} - {self.cno} - {self.grade}"