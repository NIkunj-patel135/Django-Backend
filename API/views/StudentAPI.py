from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from API.serializers.studentSerializer import StudentSerializer 
from API.models.students import Students
from API.auths.verify import VerifyToken


class StudentAPIView(APIView):
    def get(self,request,id=None):
        try:
            response = VerifyToken(request,access_type="student-access")
            if(id is not None):
                try:
                    student_obj = Students.objects.get(id=id)
                except Students.DoesNotExist:
                    raise Exception("Given id is Invalid")
                serializer = StudentSerializer(student_obj)
                response.data = {
                    "success":True,
                    "message":"Student GET request Successful",
                    "Data":serializer.data
                }
                response.status_code = status.HTTP_202_ACCEPTED
                return response
            if(request.GET.get("ids")):
                ids = request.GET.get('ids', '').split(',')
                student_objs = Students.objects.filter(id__in=ids).order_by('id')
                serializer = StudentSerializer(student_objs,many=True)
                response.data = {
                    "success":True,
                    "message":"Students GET request Successful",
                    "Data":serializer.data
                }
                response.status_code = status.HTTP_202_ACCEPTED
                return response
            
            student_objs = Students.objects.all()
            serializer = StudentSerializer(student_objs,many=True)
            response.data = {
                    "success":True,
                    "message":"Student GET request Successful",
                    "Data":serializer.data
            }
            response.status_code = status.HTTP_202_ACCEPTED
            return response
        
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({
                    'success':False,
                    "message":"Please provide token"
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
            response = VerifyToken(request,access_type="student-access")
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                response.data = {
                    'success':False,
                    'message':serializer.errors,
                }
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
                
            serializer.save()
            response.data = {
                "success":True,
                "message":"Student Data Saved"
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
            response = VerifyToken(request,access_type="student-access")
            try:
                student_obj = Students.objects.get(id=id)
            except Students.DoesNotExist:
                    raise Exception("Given id is Invalid")
            serializer = StudentSerializer(student_obj,data=request.data)
            if not serializer.is_valid():
                response.data = {
                    'success':False,
                    'message':serializer.errors,
                }
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
                
            serializer.save()
            response.data = {
                "success":True,
                "message":"Student Data Updated"
            }
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({
                    'success':False,
                    'message':'Please provide token'
                },status=status.HTTP_401_UNAUTHORIZED)
            
            if str(e) == "Refresh token expired":
                return Response({
                    "success":False,
                    "message":"Refresh token expired"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({
                "success":False,
                "message":str(e)
            },status=status.HTTP_401_UNAUTHORIZED)
        
    def patch(self,request,id):
        try:
            response = VerifyToken(request,access_type="student-access")
            try:
                student_obj = Students.objects.get(id=id)
            except Students.DoesNotExist:
                    raise Exception("Given id is Invalid")
            serializer = StudentSerializer(student_obj,data=request.data,partial=True)
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
                "message":"Student Data Updated",
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
            response = VerifyToken(request,access_type="student-access")
            try:
                student_obj = Students.objects.get(id=id)
            except Students.DoesNotExist:
                    raise Exception("Given id is Invalid")
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                response.data = {
                    'success':False,
                    'message':serializer.errors
                }
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
                
            student_obj.delete()
            response.data = {
                'success':True,
                'message':'Student Data Deleted'
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
