from django.urls import path
from .views import CourseAPIView,InstructorAPIView,StudentAPIView,LogOutAPIView
from .views import InstructorRegisterAPIView,StudentRegisterAPIView,StudentLoginAPIView,InstructorLoginAPIView
from .views import StudentAuthAPIView,InstructorAuthAPIView

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