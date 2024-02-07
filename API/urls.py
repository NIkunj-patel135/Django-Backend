from django.urls import path
from .views import CourseAPIView,InstructorAPIView,StudentAPIView,LogOutAPIView,StudentRegisterAPIView,InstructorRegisterAPIView,StudentLoginAPIView


urlpatterns = [
    path('api/v1/course/',CourseAPIView.as_view()),
    path('api/v1/course/<int:id>',CourseAPIView.as_view()),
    path('api/v1/instructor_login/',InstructorRegisterAPIView.as_view()),
    path('api/v1/instructor/',InstructorAPIView.as_view()),
    path('api/v1/instructor/<int:id>',InstructorAPIView.as_view()),
    path('api/v1/student_register/',StudentRegisterAPIView.as_view()),
    path('api/v1/student_login/',StudentLoginAPIView.as_view()),
    path('api/v1/student/<int:id>',StudentAPIView.as_view()),
    path('api/v1/student/',StudentAPIView.as_view()),
    path('api/v1/logout/',LogOutAPIView.as_view()),
]