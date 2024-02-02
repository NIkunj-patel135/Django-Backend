from django.contrib import admin
from .models import Courses,Students,Instructors

admin.site.register(Courses)
admin.site.register(Students)
admin.site.register(Instructors)