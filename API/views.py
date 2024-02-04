from .models import Courses,Students,Instructors
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .serializers import StudentSerializer,InstructorSerializer,CourseSerializer,CustomRefreshToken
from rest_framework_simplejwt.views import TokenRefreshView,TokenError, token_refresh
from datetime import datetime
from rest_framework_simplejwt.views import TokenRefreshView

# Create your views here.
class check(APIView):
    def post(self,request):
        access_token = request.COOKIES.get("access")
        refresh_token = request.COOKIES.get("refresh")
        refresh_token = AccessToken(refresh_token)
        expire = refresh_token.payload['exp']
        
        expiration_datetime = datetime.utcfromtimestamp(expire)
        # refresh_token = AccessToken(refresh_token)
        
        if expiration_datetime > datetime.utcnow():
            #new tokens are generated
            user_id = refresh_token.payload['user_id']
            user = User.objects.get(id=int(user_id))
            new_token = RefreshToken.for_user(user)
            print("new access token",str(new_token.access_token))
            print("new refresh token",str(new_token))
            print(access_token == new_token.access_token)
            
        else:
            print("Token is still valid")
        
        return Response({'status':"success"},status=status.HTTP_200_OK)
    
    def get(self,request):
        try:
            access_token = request.COOKIES.get("access")
            access_token = AccessToken(access_token)
            
        except TokenError as e: 
            # Check if the error is due to token expiration
            if str(e) == 'Token is invalid or expired':
                
                    refresh_token = request.data.get("refresh")
                    user_id = request.COOKIES.get("user_id")
                    refresh_token = RefreshToken(refresh_token)
                    user = User.objects.get(id=int(user_id))
                    new_token = RefreshToken.for_user(user)
                    print(access_token == new_token.access_token)
                    # print("new access token",AccessToken(new_token.access_token))
                    # print("new refresh token",RefreshToken(new_token))
                    return Response({"error or success":"new tokens generated"},status=200)
                # except TokenError as re:
                #     return Response({'error': 'Refresh token has expired, again login'}, status=400)
            else:
                return Response({'error': str(e)}, status=400)
        print(access_token.payload)
        return Response({"success":"token is still valid"},status=200)

class LoginAPIView(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        user = User(username=username)
        user.set_password(str(password))
        user.save()
        token = CustomRefreshToken.for_user(user)
        response = Response()
        response.set_cookie('access',str(token.access_token),httponly=True)
        response.set_cookie('refresh',str(token),httponly=True)
        response.set_cookie('user_id',user.id,httponly=True)
        
        return response


class CourseAPIView(APIView):
    def get(self,request):
        try:
            course_objs = Courses.objects.all()
            serializer = CourseSerializer(course_objs,many=True)
            
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request):
        try:
            serializer = CourseSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response("Data Saved",status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,id):
        try:
            course_obj = Courses.objects.get(id=id)
            serializer = CourseSerializer(course_obj,data=request.data)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,id):
        try:
            course_obj = Courses.objects.get(id=id)
            serializer = CourseSerializer(course_obj,data=request.data,partial=True)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        try:
            course_obj = Courses.objects.get(id=id)
            serializer = CourseSerializer(course_obj,data=request.data)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            course_obj.delete()
            return Response({'message':'Data Deleted',"status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'Provide Valid Data','status':404},status=status.HTTP_404_NOT_FOUND)

class InstructorAPIView(APIView):
    
    def get(self,request):
        try:
            instructor_objs = Instructors.objects.all()
            serializer = InstructorSerializer(instructor_objs,many=True)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        try:
            serializer = InstructorSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response("Data Saved",status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,id):
        try:
            instructor_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(instructor_obj,data=request.data)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,id):
        try:
            instructor_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(instructor_obj,data=request.data,partial=True)
            if not serializer.is_valid():
                return Response({"message":serializer.erros,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        try:
            instructor_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"error":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            instructor_obj.delete()
            return Response({'message':'Data Deleted',"status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'Provide Valid Data','status':404},status=status.HTTP_404_NOT_FOUND)

class StudentAPIView(APIView):
    def get(self,request):
        try:
            student_objs = Students.objects.all()
            serializer = StudentSerializer(student_objs,many=True)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        try:
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response("Data Saved",status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,id):
        try:
            student_obj = Students.objects.get(id=id)
            serializer = StudentSerializer(student_obj,data=request.data)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def patch(self,request,id):
        try:
            student_obj = Students.objects.get(id=id)
            serializer = InstructorSerializer(student_obj,data=request.data,partial=True)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def delete(self,request,id):
        try:
            student_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"error":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            student_obj.delete()
            return Response({'message':'Data Deleted',"status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'Provide Valid Data','status':404},status=status.HTTP_404_NOT_FOUND)
