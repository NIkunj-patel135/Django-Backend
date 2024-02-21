from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from API.serializers.instructorSerializer import InstructorSerializer
from API.models.instructors import Instructors
from API.auths.verify import VerifyToken




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
