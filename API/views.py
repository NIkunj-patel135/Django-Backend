from .models import Courses,Students,Instructors
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .serializers import StudentSerializer,InstructorSerializer,CourseSerializer
from rest_framework_simplejwt.views import TokenError
from django.contrib.auth.hashers import check_password


def VerifyToken(request,access_type=None):
    try:
        if(access_type is not None):
            if(access_type != request.COOKIES.get('access-type')):
                raise Exception("Unauthorized access")
        access_token = request.COOKIES.get("access")
        if access_token is None:
            raise Exception("Please provide token")

        access_token = AccessToken(access_token)
        
        return Response()
    except TokenError as e:        
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


class StudentAuthAPIView(APIView):
    def get(self,request):
        try:
            response = VerifyToken(request,'student-access')
            student_id = request.COOKIES.get('user_id')
            try:
                student_obj = Students.objects.get(id=student_id)
            except Students.DoesNotExist:
                raise Exception("Given id is InValid")
            serializer = StudentSerializer(student_obj)
            response.data = {"data":serializer.data}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)
        
class InstructorAuthAPIView(APIView):
    def get(self,request):
        try:
            response = VerifyToken(request,'instructor-access')
            instructor_id = request.COOKIES.get('user_id')
            try:
                instructor_obj = Instructors.objects.get(id=instructor_id)
            except Instructors.DoesNotExist:
                raise Exception("Given id is InValid")
            serializer = StudentSerializer(instructor_obj)
            response.data = {"data":serializer.data}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)
        

class StudentRegisterAPIView(APIView):
    def post(self,request):
        try:
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
            return Response({},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)

class InstructorRegisterAPIView(APIView):
    def post(self,request):
        try:
            serializer = InstructorSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
            return Response({},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)

class StudentLoginAPIView(APIView):
    def post(self,request):
        username = request.data['name']
        password = request.data['password']
        try:
            student = Students.objects.get(name=username)
            if(not check_password(password,student.password)):
                raise Exception("password is wrong")
            token = RefreshToken.for_user(student)
            response = Response()
            response.set_cookie('access',str(token.access_token),httponly=True,secure=True)
            response.set_cookie('refresh',str(token),httponly=True,secure=True)
            response.set_cookie('access-type','student-access',httponly=True,secure=True)
            response.set_cookie('user_id',student.id,httponly=True,secure=True)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_401_UNAUTHORIZED)

        return response

class InstructorLoginAPIView(APIView):
    def post(self,request):
        username = request.data['name']
        password = request.data['password']
        email = request.data["email"]
        try:
            instructor = Instructors.objects.get(email=email)
            if(not check_password(password,instructor.password)):
                raise Exception("password is wrong")
            
            token = RefreshToken.for_user(instructor)
            response = Response()
            response.set_cookie('access',str(token.access_token),httponly=True,secure=True)
            response.set_cookie('refresh',str(token),httponly=True,secure=True)
            response.set_cookie('access-type',"instructor-access",httponly=True,secure=True)
            response.set_cookie('user_id',instructor.id,httponly=True,secure=True)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_401_UNAUTHORIZED)
        return response

class LogOutAPIView(APIView):
    def get(self,request):
        response = Response()
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        response.delete_cookie('user_id')
        response.delete_cookie('access-type')
        response.data = {"logout successful"}
        return response



class CourseAPIView(APIView):
    def get(self,request,id=None):
        try:
            response = VerifyToken(request)
            if(id is not None):
                try:
                    course_objs = Courses.objects.get(id=id)
                except Courses.DoesNotExist:
                    raise Exception("Given id is Invalid")
                serializer = CourseSerializer(course_objs)
                response.data = {"data":serializer.data}
                response.status_code = status.HTTP_202_ACCEPTED
                return response
            
            if(request.GET.get("ids")):
                ids = request.GET.get('ids', '').split(',')
                course_objs = Courses.objects.filter(id__in=ids).order_by('id')
                serializer = CourseSerializer(course_objs,many=True)
                response.data = {"data":serializer.data}
                response.status_code = status.HTTP_202_ACCEPTED
                return response 

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
            
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request):
        try:

            response = VerifyToken(request)
            instructor_id=request.COOKIES.get('user_id')
            serializer = CourseSerializer(data = request.data)
            if  not serializer.is_valid():
                response.data = {'error':serializer.errors}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
            serializer.save(instructor_id=instructor_id)
            response.data = "Data Saved"
            response.status_code = status.HTTP_201_CREATED
            return response
        except Exception as e:

            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,id):
        try:
            response = VerifyToken(request)
            try:
                course_obj = Courses.objects.get(id=id)
            except Courses.DoesNotExist:
                    raise Exception("Given id is Invalid")
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
            
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,id):
        try:
            response = VerifyToken(request)
            try:
                course_obj = Courses.objects.get(id=id)
            except Courses.DoesNotExist:
                    raise Exception("Given id is Invalid")
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
            
            return Response({'error':str(e),"status":404},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        try:
            response = VerifyToken(request)
            try:
                course_obj = Courses.objects.get(id=id)
            except Courses.DoesNotExist:
                    raise Exception("Given id is Invalid")
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
                        
            return Response({'message':str(e),'status':404},status=status.HTTP_404_NOT_FOUND)

class InstructorAPIView(APIView):
    
    def get(self,request,id=None):
        try:
            response = VerifyToken(request,access_type = "instructor-access")
            if(id is not None):
                try:
                    instructor_objs = Instructors.objects.get(id=id)
                except Instructors.DoesNotExist:
                    raise Exception("Given id is Invalid")
                serializer = InstructorSerializer(instructor_objs)
                response.data = {"data":serializer.data}
                response.status_code = status.HTTP_202_ACCEPTED
                return response
            
            if(request.GET.get("ids")):
                ids = request.GET.get('ids', '').split(',')
                instructor_objs = Instructors.objects.filter(id__in=ids).order_by('id')
                serializer = InstructorSerializer(instructor_objs,many=True)
                response.data = {"data":serializer.data}
                response.status_code = status.HTTP_202_ACCEPTED
                return response
            
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
             
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        try:
            response = VerifyToken(request,access_type = "instructor-access")
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
            
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,id):
        try:
            response = VerifyToken(request,access_type="instructor-access")
            try:
                instructor_obj = Instructors.objects.get(id=id)
            except Instructors.DoesNotExist:
                    raise Exception("Given id is Invalid")
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
            
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,id):
        try:
            response = VerifyToken(request,access_type="instructor-access")
            try:
                instructor_obj = Instructors.objects.get(id=id)
            except Instructors.DoesNotExist:
                    raise Exception("Given id is Invalid")
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
            
            return Response({'error':str(e),"status":404},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        try:
            response = VerifyToken(request,access_type="instructor-access")
            try:
                instructor_obj = Instructors.objects.get(id=id)
            except Instructors.DoesNotExist:
                    raise Exception("Given id is Invalid")
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
            
            return Response({'message':str(e),'status':404},status=status.HTTP_404_NOT_FOUND)

class StudentAPIView(APIView):
    def get(self,request,id=None):
        try:
            response = VerifyToken(request,access_type="student-access")
            if(id is not None):
                try:
                    student_obj = Students.objects.get(id=id)
                    print(student_obj)
                except Students.DoesNotExist:
                    raise Exception("Given id is Invalid")
                serializer = StudentSerializer(student_obj)
                response.data = {"data":serializer.data}
                response.status_code = status.HTTP_202_ACCEPTED
                return response
            if(request.GET.get("ids")):
                ids = request.GET.get('ids', '').split(',')
                student_objs = Students.objects.filter(id__in=ids).order_by('id')
                serializer = StudentSerializer(student_objs,many=True)
                response.data = {"data":serializer.data}
                response.status_code = status.HTTP_202_ACCEPTED
                return response
            
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
            
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        try:
            response = VerifyToken(request,access_type="student-access")
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
            
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,id):
        try:
            response = VerifyToken(request,access_type="student-access")
            try:
                student_obj = Students.objects.get(id=id)
            except Students.DoesNotExist:
                    raise Exception("Given id is Invalid")
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
            
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)
        
    def patch(self,request,id):
        try:
            response = VerifyToken(request,access_type="student-access")
            try:
                student_obj = Students.objects.get(id=id)
            except Students.DoesNotExist:
                    raise Exception("Given id is Invalid")
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
            
            return Response({'error':str(e),"status":404},status=status.HTTP_404_NOT_FOUND)
    def delete(self,request,id):
        try:
            response = VerifyToken(request,access_type="student-access")
            try:
                student_obj = Instructors.objects.get(id=id)
            except Students.DoesNotExist:
                    raise Exception("Given id is Invalid")
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
            
            return Response({'message':str(e),'status':404},status=status.HTTP_404_NOT_FOUND)
