from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from API.serializers.studentSerializer import StudentSerializer


class StudentRegisterAPIView(APIView):
    def post(self,request):
        try:
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success':False,
                    'message':serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
            return Response({
                "success":True,
                "message":"Student Register successful"
            },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "success":False,
                "message":str(e)
            },status=status.HTTP_404_NOT_FOUND)
