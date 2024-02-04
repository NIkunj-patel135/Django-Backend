from django.urls import path,include
from .views import CourseAPIView,InstructorAPIView,StudentAPIView,LoginAPIView,check


urlpatterns = [
    path('api/v1/course/',CourseAPIView.as_view()),
    path('api/v1/course/<int:id>',CourseAPIView.as_view()),
    path('api/v1/instructor/',InstructorAPIView.as_view()),
    path('api/v1/instructor/<int:id>',InstructorAPIView.as_view()),
    path('api/v1/student/<int:id>',StudentAPIView.as_view()),
    path('api/v1/student/',StudentAPIView.as_view()),
    path('api/v1/login/',LoginAPIView.as_view()),
    path('api/v1/check/',check.as_view())
]