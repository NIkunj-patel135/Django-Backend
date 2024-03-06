from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from API.models.instructors import Instructors
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

class InstructorLoginAPIView(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            password = request.data['password']
            instructor = Instructors.objects.get(email=email)
            if(not check_password(password,instructor.password)):
                raise Exception("password is wrong")
            
            token = RefreshToken.for_user(instructor)
            response = Response()
            response.data = {
                "success":True,
                "message":"Instructor Login Successful"
            }
            response.status_code = status.HTTP_200_OK
            response.set_cookie('access',str(token.access_token),httponly=True,secure=True)
            response.set_cookie('refresh',str(token),httponly=True,secure=True)
            response.set_cookie('access-type',"instructor-access",httponly=True,secure=True)
            response.set_cookie('user_id',instructor.id,httponly=True,secure=True)
        except Exception as e:
            return Response({
                "success":False,
                "message":str(e)
            },status=status.HTTP_401_UNAUTHORIZED)
        return response
