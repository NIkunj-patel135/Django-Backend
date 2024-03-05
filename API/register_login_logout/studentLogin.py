from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from API.models.students import Students
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


class StudentLoginAPIView(APIView):
    def post(self,request):
        try:
            username = request.data['name']
            password = request.data['password']
            student = Students.objects.get(name=username)
            if(not check_password(password,student.password)):
                raise Exception("password is wrong")
            token = RefreshToken.for_user(student)
            response = Response()
            response.data = {
                "success":True,
                "message":"Student Login successful"
            }
            response.status_code = status.HTTP_200_OK
            response.set_cookie('access',str(token.access_token),httponly=True,secure=True)
            response.set_cookie('refresh',str(token),httponly=True,secure=True)
            response.set_cookie('access-type','student-access',httponly=True,secure=True)
            response.set_cookie('user_id',student.id,httponly=True,secure=True)
        except Exception as e:
            return Response({
                "success":False,
                "message":str(e)
            },status=status.HTTP_401_UNAUTHORIZED)

        return response
