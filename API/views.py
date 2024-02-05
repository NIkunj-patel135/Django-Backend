from .models import Courses,Students,Instructors
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .serializers import StudentSerializer,InstructorSerializer,CourseSerializer,CustomRefreshToken
from rest_framework_simplejwt.views import TokenRefreshView,TokenError
from datetime import datetime
import jwt
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
            print(access_token)
            access_token = AccessToken(access_token)
            print(request.COOKIES)
            return Response({"success":"token is still valid"},status=200)
        except TokenError as e: 
            # Check if the error is due to token expiration
            # if str(e) == 'Token is invalid or expired': 
            #         user_id = request.COOKIES.get("user_id")
                    
            #         user = User.objects.get(id=int(user_id))
            #         new_access = RefreshToken.for_user(user)
            #         print(new_access.access_token)
            #         response = Response()
            #         response.set_cookie('access',str(new_access.access_token),httponly=True)
            #         response.set_cookie('refresh',str(new_access),httponly=True)
            #         return response
            # else:
            #     return Response({'error': str(e)}, status=400)
            
            try:
                if(RefreshToken(request.COOKIES.get('refresh'))):
                    user_id = request.COOKIES.get("user_id")
                    user = User.objects.get(id=int(user_id))
                    new_access = RefreshToken.for_user(user)
                    print(new_access.access_token)
                    response = Response()
                    response.set_cookie('access',str(new_access.access_token),httponly=True)
                    response.set_cookie('refresh',str(new_access),httponly=True)
                    return response
            except TokenError as e:
                return Response({"reason":"refresh token expired"},status=400)
            


class LoginAPIView(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        user = User(username=username)
        user.set_password(str(password))
        user.save()
        token = RefreshToken.for_user(user)
        response = Response()
        response.set_cookie('access',str(token.access_token),httponly=True)
        response.set_cookie('refresh',str(token),httponly=True)
        response.set_cookie('user_id',user.id,httponly=True)
        return response

class LogOutAPIView(APIView):
    def get(self,request):
        response = Response()
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        response.delete_cookie('user_id')
        response.data = {"logout successful"}
        return response

def VerifyToken(request):
    try:
        access_token = request.COOKIES.get("access")
        if access_token is None:
            raise Exception("Please provide token")

        access_token = AccessToken(access_token)
        
        return Response()
    except TokenError as e: 
        # Check if the error is due to token expiration
        # if str(e) == 'Token is invalid or expired': 
        #         user_id = request.COOKIES.get("user_id")
            
        #         user = User.objects.get(id=int(user_id))
        #         new_access = RefreshToken.for_user(user)
        #         print(new_access.access_token)
        #         response = Response()
        #         response.set_cookie('access',str(new_access.access_token),httponly=True)
        #         response.set_cookie('refresh',str(new_access),httponly=True)
        #         return response
        # else:
        #     return Response({'error': str(e)}, status=400)
        
        try:
            if(RefreshToken(request.COOKIES.get('refresh'))):
                user_id = request.COOKIES.get("user_id")
                user = User.objects.get(id=int(user_id))
                new_access = RefreshToken.for_user(user)
                print(new_access.access_token)
                response = Response()
                response.set_cookie('access',str(new_access.access_token),httponly=True)
                response.set_cookie('refresh',str(new_access),httponly=True)
                return response
        except TokenError as e:
                raise Exception("Refresh token expired")


class CourseAPIView(APIView):
    def get(self,request):
        try:

            response = VerifyToken(request)
            course_objs = Courses.objects.all()
            serializer = CourseSerializer(course_objs,many=True)
            response.data = {"data":serializer.data}
            response.status_code = status.HTTP_202_ACCEPTED
            return response 
        
        except Exception as e:

            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request):
        try:

            response = VerifyToken(request)
            serializer = CourseSerializer(data = request.data)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
            
            serializer.save()
            response.data = "Data Saved"
            response.status_code = status.HTTP_201_CREATED
            return response
        except Exception as e:

            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,id):
        try:
            response = VerifyToken(request)
            course_obj = Courses.objects.get(id=id)
            serializer = CourseSerializer(course_obj,data=request.data)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
            serializer.save()
            response.data = {"message":"Data Updated","status":200}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:

            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,id):
        try:
            response = VerifyToken(request)
            course_obj = Courses.objects.get(id=id)
            serializer = CourseSerializer(course_obj,data=request.data,partial=True)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
    
            serializer.save()
            response.data = {"message":"Data Updated","status":200}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:

            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({'error':"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        try:
            response = VerifyToken(request)
            course_obj = Courses.objects.get(id=id)
            serializer = CourseSerializer(course_obj,data=request.data)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
                
            course_obj.delete()
            response.data = {'message':'Data Deleted',"status":200}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:

            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
                        
            return Response({'message':'Provide Valid Data','status':404},status=status.HTTP_404_NOT_FOUND)

class InstructorAPIView(APIView):
    
    def get(self,request):
        try:
            response = VerifyToken(request)
            instructor_objs = Instructors.objects.all()
            serializer = InstructorSerializer(instructor_objs,many=True)
            response.data = {"data":serializer.data}
            response.status_code = status.HTTP_202_ACCEPTED
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
             
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        try:
            response = VerifyToken(request)
            serializer = InstructorSerializer(data = request.data)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
                
            serializer.save()
            response.data = "Data Saved"
            response.status_code = status.HTTP_201_CREATED
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,id):
        try:
            response = VerifyToken(request)
            instructor_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(instructor_obj,data=request.data)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
            serializer.save()
            response.data = {"message":"Data Updated","status":200}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,id):
        try:
            response = VerifyToken(request)
            instructor_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(instructor_obj,data=request.data,partial=True)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
                
            serializer.save()
            response.data = {"message":"Data Updated","status":200}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({'error':"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        try:
            response = VerifyToken(request)
            instructor_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(data=request.data)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
                
            instructor_obj.delete()
            response.data = {'message':'Data Deleted'}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({'message':'Provide Valid Data','status':404},status=status.HTTP_404_NOT_FOUND)

class StudentAPIView(APIView):
    def get(self,request):
        try:
            response = VerifyToken(request)
            student_objs = Students.objects.all()
            serializer = StudentSerializer(student_objs,many=True)
            response.data = {"data":serializer.data}
            response.status_code = status.HTTP_202_ACCEPTED
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        try:
            response = VerifyToken(request)
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
                
            serializer.save()
            response.data = {"Data Saved"}
            response.status_code = status.HTTP_201_CREATED
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,id):
        try:
            response = VerifyToken(request)
            student_obj = Students.objects.get(id=id)
            serializer = StudentSerializer(student_obj,data=request.data)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
                
            serializer.save()
            response.data = {"message":"Data Updated"}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
        
    def patch(self,request,id):
        try:
            response = VerifyToken(request)
            student_obj = Students.objects.get(id=id)
            serializer = InstructorSerializer(student_obj,data=request.data,partial=True)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
            
            serializer.save()
            response.data = {"message":"Data Updated"}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({'error':"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def delete(self,request,id):
        try:
            response = VerifyToken(request)
            student_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(data=request.data)
            if not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
                
            student_obj.delete()
            response.data = {'message':'Data Deleted'}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({'message':'Provide Valid Data','status':404},status=status.HTTP_404_NOT_FOUND)
