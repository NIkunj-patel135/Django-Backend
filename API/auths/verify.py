from API.models.students import Students
from API.models.instructors import Instructors
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.views import TokenError
from rest_framework.response import Response


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

                if(access_type == "student-access"):
                    user = Students.objects.get(id=int(user_id))
                else:
                    user = Instructors.objects.get(id=int(user_id))

                new_access = RefreshToken.for_user(user)
                response = Response()
                response.set_cookie('access',str(new_access.access_token),httponly=True)
                response.set_cookie('refresh',str(new_access),httponly=True)
                return response
        except TokenError as e:
                raise Exception("Refresh token expired")
