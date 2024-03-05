from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from API.serializers.instructorSerializer import InstructorSerializer 

class InstructorRegisterAPIView(APIView):
    def post(self,request):
        try:
            serializer = InstructorSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({
                    'success':False,
                    'message':serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
            return Response({
                "success":True,
                "message":"Instructor Register Successful"
            },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "success":False,
                "message":str(e)
            },status=status.HTTP_404_NOT_FOUND)
