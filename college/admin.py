from django.contrib import admin
from college.models import  Student , Course, Enrol

@admin.register(Student)
class  StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class  CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Enrol)
class  EnrolAdmin(admin.ModelAdmin):
    pass
