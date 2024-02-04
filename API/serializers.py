from rest_framework import serializers
from .models import Students,Instructors,Courses
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
#validate - common validation to all fields is check for sql injection by using validate() and loop through every

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['user_id'] = str(user.id)  # Include the user ID in the token payload
        return token





class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'

    def validate(self,data):
        errors = {}
        for field,value in data.items():
            if ';' in value or 'select' in value or '*' in value or '--' in value:
                errors[field] = "provide valid character"
        if errors:
            raise serializers.ValidationError(errors)
        return data
        
class InstructorSerializer(serializers.ModelSerializer):
    courses_taught = CourseSerializer(many=True)

    class Meta:
        model = Instructors
        fields = '__all__'

    def validate(self,data):
        errors = {}
        for field,value in data.items():
            if ';' in value or 'select' in value or '*' in value or '--' in value:
                errors[field] = "provide valid character"
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
    def create(self,validated_data):
        courses_data = validated_data.pop('courses_taught')
        instructor = Instructors.objects.create(**validated_data)
        for course_data in courses_data:
            course,created = Courses.objects.get_or_create(**course_data)
            instructor.courses_taught.add(course)
        return instructor 

class StudentSerializer(serializers.ModelSerializer):
    courses_enrolled = CourseSerializer(many=True)

    class Meta:
        model = Students
        fields = '__all__'

    def validate(self,data):
        errors = {}
        for field,value in data.items():
            if ';' in value or 'select' in value or '*' in value or '--' in value:
                errors[field] = "provide valid character"
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self,validated_data):
        password = validated_data.pop('password')
        courses_data = validated_data.pop('courses_enrolled')
        student = Students.objects.create(password=make_password(password),**validated_data)
        for course_data in courses_data:
            course,created = Courses.objects.get_or_create(**course_data)
            student.courses_enrolled.add(course)
        return student