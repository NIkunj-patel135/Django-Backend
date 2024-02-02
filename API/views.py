from .models import Courses,Students,Instructors
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import StudentSerializer,InstructorSerializer,CourseSerializer
# Create your views here.

class CourseAPIView(APIView):
    def get(self,request):
        try:
            course_objs = Courses.objects.all()
            serializer = CourseSerializer(course_objs,many=True)
            
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request):
        try:
            serializer = CourseSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response("Data Saved",status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,id):
        try:
            course_obj = Courses.objects.get(id=id)
            serializer = CourseSerializer(course_obj,data=request.data)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,id):
        try:
            course_obj = Courses.objects.get(id=id)
            serializer = CourseSerializer(course_obj,data=request.data,partial=True)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        try:
            course_obj = Courses.objects.get(id=id)
            serializer = CourseSerializer(course_obj,data=request.data)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            course_obj.delete()
            return Response({'message':'Data Deleted',"status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'Provide Valid Data','status':404},status=status.HTTP_404_NOT_FOUND)

class InstructorAPIView(APIView):
    
    def get(self,request):
        try:
            instructor_objs = Instructors.objects.all()
            serializer = InstructorSerializer(instructor_objs,many=True)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        try:
            serializer = InstructorSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response("Data Saved",status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,id):
        try:
            instructor_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(instructor_obj,data=request.data)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,id):
        try:
            instructor_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(instructor_obj,data=request.data,partial=True)
            if not serializer.is_valid():
                return Response({"message":serializer.erros,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        try:
            instructor_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"error":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            instructor_obj.delete()
            return Response({'message':'Data Deleted',"status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'Provide Valid Data','status':404},status=status.HTTP_404_NOT_FOUND)

class StudentAPIView(APIView):
    def get(self,request):
        try:
            student_objs = Students.objects.all()
            serializer = StudentSerializer(student_objs,many=True)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        try:
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response("Data Saved",status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,id):
        try:
            student_obj = Students.objects.get(id=id)
            serializer = StudentSerializer(student_obj,data=request.data)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def patch(self,request,id):
        try:
            student_obj = Students.objects.get(id=id)
            serializer = InstructorSerializer(student_obj,data=request.data,partial=True)
            if not serializer.is_valid():
                return Response({"message":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response({"message":"Data Updated","status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':"Provide Valid Data","status":404},status=status.HTTP_404_NOT_FOUND)
    def delete(self,request,id):
        try:
            student_obj = Instructors.objects.get(id=id)
            serializer = InstructorSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"error":serializer.errors,"status":404},status=status.HTTP_404_NOT_FOUND)
            student_obj.delete()
            return Response({'message':'Data Deleted',"status":200},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'Provide Valid Data','status':404},status=status.HTTP_404_NOT_FOUND)
