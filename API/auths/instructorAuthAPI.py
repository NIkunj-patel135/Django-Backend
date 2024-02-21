from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from API.serializers.instructorSerializer import InstructorSerializer 
from API.models.instructors import Instructors 
from API.auths.verify import VerifyToken 


class InstructorAuthAPIView(APIView):
    def get(self,request):
        try:
            response = VerifyToken(request,'instructor-access')
            instructor_id = request.COOKIES.get('user_id')
            try:
                instructor_obj = Instructors.objects.get(id=instructor_id)
            except Instructors.DoesNotExist:
                raise Exception("Given id is InValid")
            serializer = InstructorSerializer(instructor_obj)
            response.data = {"data":serializer.data}
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:
            if str(e) == "Please provide token":
                return Response({'token error':"Please provide token"})
            
            if str(e) == "Refresh token expired":
                return Response({"token error":"Refresh token expired"},status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)
     