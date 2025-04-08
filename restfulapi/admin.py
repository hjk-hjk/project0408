from django.contrib import admin
from restfulapi.models import  Student , Course, Enrol

@admin.register(Student)
class  StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class  CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Enrol)
class  EnrolAdmin(admin.ModelAdmin):
    pass