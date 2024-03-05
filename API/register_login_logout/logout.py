from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class LogOutAPIView(APIView):
    def get(self,request):
        response = Response()
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        response.delete_cookie('user_id')
        response.delete_cookie('access-type')
        response.data = {
            "success":True,
            "message":"logout successful"
        }
        response.status_code = status.HTTP_200_OK
        return response
