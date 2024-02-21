from django.contrib import admin
from .models.courses import Courses
from .models.students import Students
from .models.instructors import Instructors

admin.site.register(Courses)
admin.site.register(Students)
admin.site.register(Instructors)