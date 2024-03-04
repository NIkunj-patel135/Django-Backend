from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from API.serializers.courseSerializer import CourseSerializer
from API.models.courses import Courses
from API.auths.verify import VerifyToken 


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
                response.data = {
                    "success":True,
                    "message":"Course GET request successful",
                    "Data":serializer.data
                }
                response.status_code = status.HTTP_202_ACCEPTED
                return response
            
            if(request.GET.get("ids")):
                ids = request.GET.get('ids', '').split(',')
                course_objs = Courses.objects.filter(id__in=ids).order_by('id')
                serializer = CourseSerializer(course_objs,many=True)
                response.data = {
                    "success":True,
                    "message":"Courses GET request successful",
                    "Data":serializer.data
                }
                response.status_code = status.HTTP_202_ACCEPTED
                return response 

            course_objs = Courses.objects.all()
            serializer = CourseSerializer(course_objs,many=True)
            response.data = {
                "success":True,
                "message":"Courses GET request successful",
                "Data":serializer.data
            }
            response.status_code = status.HTTP_202_ACCEPTED
            return response 
        
        except Exception as e:

            if str(e) == "Please provide token":
                return Response({
                    'success':False,
                    'message':"Please provide token"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            if str(e) == "Refresh token expired":
                return Response({
                    "success":False,
                    "message":"Refresh token expired"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({
                "success":False,
                "message":str(e)
            },status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request):
        try:

            response = VerifyToken(request)
            instructor_id=request.COOKIES.get('user_id')
            serializer = CourseSerializer(data = request.data)
            if  not serializer.is_valid():
                response.data = {
                    'success':False,
                    'message':serializer.errors
                }
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
            serializer.save(instructor_id=instructor_id)
            response.data = {
                    'success':True,
                    'message':'Course Data Saved'
            }
            response.status_code = status.HTTP_201_CREATED
            return response
        except Exception as e:

            if str(e) == "Please provide token":
                return Response({
                    'success':False,
                    'message':"Please provide token"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            if str(e) == "Refresh token expired":
                return Response({
                    "success":False,
                    "message":"Refresh token expired"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({
                "success":False,
                "message":str(e)
            },status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,id):
        try:
            response = VerifyToken(request)
            try:
                course_obj = Courses.objects.get(id=id)
            except Courses.DoesNotExist:
                    raise Exception("Given id is Invalid")
            serializer = CourseSerializer(course_obj,data=request.data)
            if not serializer.is_valid():
                response.data = {
                    'success':False,
                    'message':serializer.errors
                }
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
            serializer.save()
            response.data = {
                "success":True,
                "message":"Course Data Updated"
            }
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:

            if str(e) == "Please provide token":
                return Response({
                    'success':False,
                    'message':"Please provide token"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            if str(e) == "Refresh token expired":
                return Response({
                    "success":False,
                    "message":"Refresh token expired"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({
                "success":False,
                "message":str(e)
            },status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,id):
        try:
            response = VerifyToken(request)
            try:
                course_obj = Courses.objects.get(id=id)
            except Courses.DoesNotExist:
                    raise Exception("Given id is Invalid")
            serializer = CourseSerializer(course_obj,data=request.data,partial=True)
            if not serializer.is_valid():
                response.data = {
                    'success':False,
                    'message':serializer.errors
                }
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
    
            serializer.save()
            response.data = {
                "success":True,
                "message":"Course Data Updated"
            }
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:

            if str(e) == "Please provide token":
                return Response({
                    'success':False,
                    'message':"Please provide token"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            if str(e) == "Refresh token expired":
                return Response({
                    "success":False,
                    "message":"Refresh token expired"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({
                'success':False,
                'message':str(e)
            },status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        try:
            response = VerifyToken(request)
            try:
                course_obj = Courses.objects.get(id=id)
            except Courses.DoesNotExist:
                    raise Exception("Given id is Invalid")
            serializer = CourseSerializer(course_obj,data=request.data)
            if not serializer.is_valid():
                response.data = {
                    'success':False,
                    'message':serializer.errors
                }
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
                
            course_obj.delete()
            response.data = {
                'success':True,
                'message':'Course Data Deleted'
            }
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:

            if str(e) == "Please provide token":
                return Response({
                    'success':False,
                    'message':"Please provide token"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            if str(e) == "Refresh token expired":
                return Response({
                    "success":False,
                    "message":"Refresh token expired"
                },status=status.HTTP_401_UNAUTHORIZED)
                        
            return Response({
                'success':False,
                'message':str(e)
            },status=status.HTTP_404_NOT_FOUND)
