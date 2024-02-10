from rest_framework import serializers
from .models import Students,Instructors,Courses
from django.contrib.auth.hashers import make_password
import re


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'

    def validate(self,data):
        for value in data.values():
            if isinstance(value, str):
                if re.search(r';|DROP TABLE|ALTER TABLE|UPDATE|DELETE|TRUNCATE|INSERT|SELECT|CREATE TABLE', value, re.IGNORECASE):
                    raise serializers.ValidationError("Input contains potentially harmful SQL characters or queries.")
        return data
    
    def create(self,validated_data):
        
        validated_data['instructor_id'] = validated_data.get('instructor_id')
        print(validated_data['instructor_id'])
        return Courses.objects.create(**validated_data)
        
class InstructorSerializer(serializers.ModelSerializer):
    courses_taught = CourseSerializer(many=True)

    class Meta:
        model = Instructors
        fields = '__all__'


    def validate_email(self,data):
        
        email_check = Instructors.objects.filter(email=data).exists()
        if not email_check:
            return data
        raise Exception("Email already exists")
    
    def validate_phone(self,data):
        
        phone_check = Instructors.objects.filter(phone=data).exists()
        if not phone_check:
            return data
        raise Exception("Phone number already exists")


    def validate(self,data):
        for value in data.values():
            if isinstance(value, str):
                if re.search(r';|DROP TABLE|ALTER TABLE|UPDATE|DELETE|TRUNCATE|INSERT|SELECT|CREATE TABLE', value, re.IGNORECASE):
                    raise serializers.ValidationError("Input contains potentially harmful SQL characters or queries.")
        return data
    
    def create(self,validated_data):
        password = validated_data.pop('password')
        courses_data = validated_data.pop('courses_taught')
        instructor = Instructors.objects.create(password=make_password(password),**validated_data)
        for course_data in courses_data:
            course,created = Courses.objects.get_or_create(**course_data)
            instructor.courses_taught.add(course)
        return instructor 

class StudentSerializer(serializers.ModelSerializer):
    courses_enrolled = CourseSerializer(many=True)

    class Meta:
        model = Students
        fields = '__all__'

    def validate_email(self,data):
        
        email_check = Students.objects.filter(email=data).exists()
        if not email_check:
            return data
        raise Exception("Email already exists")
    
    def validate_phone(self,data):
    
        phone_check = Students.objects.filter(phone=data).exists()
        if not phone_check:
            return data
        raise Exception("Phone number already exists")

    def validate(self,data):
        for value in data.values():
            if isinstance(value, str):
                if re.search(r';|DROP TABLE|ALTER TABLE|UPDATE|DELETE|TRUNCATE|INSERT|SELECT|CREATE TABLE', value, re.IGNORECASE):
                    raise serializers.ValidationError("Input contains potentially harmful SQL characters or queries.")
        return data

    def create(self,validated_data):
        password = validated_data.pop('password')
        courses_data = validated_data.pop('courses_enrolled')
        student = Students.objects.create(password=make_password(password),**validated_data)
        for course_data in courses_data:
            course,created = Courses.objects.get_or_create(**course_data)
            student.courses_enrolled.add(course)
        return student