from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from API.serializers.studentSerializer import StudentSerializer


class StudentRegisterAPIView(APIView):
    def post(self,request):
        try:
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
            return Response({"success"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e),"status":404},status=status.HTTP_404_NOT_FOUND)
