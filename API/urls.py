from django.urls import path
from .views.CourseAPI import CourseAPIView
from .views.InstructorAPI import InstructorAPIView
from .views.StudentAPI import StudentAPIView 
from .auths.instructorAuthAPI import InstructorAuthAPIView
from .auths.studentAuthAPI import StudentAuthAPIView
from .register_login_logout.studentRegister import StudentRegisterAPIView
from .register_login_logout.instructorRegister import InstructorRegisterAPIView
from .register_login_logout.studentLogin import StudentLoginAPIView
from .register_login_logout.instructorLogin import InstructorLoginAPIView
from .register_login_logout.logout import LogOutAPIView



urlpatterns = [
    path('api/v1/course/',CourseAPIView.as_view()),
    path('api/v1/course/<int:id>',CourseAPIView.as_view()),
    path('api/v1/instructor_login/',InstructorLoginAPIView.as_view()),
    path('api/v1/instructor_register/',InstructorRegisterAPIView.as_view()),
    path('api/v1/instructor/',InstructorAPIView.as_view()),
    path('api/v1/instructor/<int:id>',InstructorAPIView.as_view()),
    path('api/v1/student_register/',StudentRegisterAPIView.as_view()),
    path('api/v1/student_login/',StudentLoginAPIView.as_view()),
    path('api/v1/student/<int:id>',StudentAPIView.as_view()),
    path('api/v1/student/',StudentAPIView.as_view()),
    path('api/v1/logout/',LogOutAPIView.as_view()),
    path('api/v1/student/auth/',StudentAuthAPIView.as_view()),
    path('api/v1/instructor/auth/',InstructorAuthAPIView.as_view())
]