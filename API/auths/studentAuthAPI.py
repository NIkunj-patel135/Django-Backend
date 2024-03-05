from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from API.serializers.studentSerializer import StudentSerializer
from API.models.students import Students
from API.auths.verify import VerifyToken 


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
            response.data = {
                "success":True,
                "message":"Student auth request successful",
                "Data":serializer.data
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
 