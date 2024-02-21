from rest_framework import serializers
from API.models.instructors import Instructors
from API.models.courses import Courses
from .courseSerializer import CourseSerializer
from django.contrib.auth.hashers import make_password
import re



class InstructorSerializer(serializers.ModelSerializer):
    courses_taught = CourseSerializer(many=True)

    class Meta:
        model = Instructors
        fields = '__all__'


    def validate_email(self,data):
        instance = self.instance
        if instance is not None and instance.email == data:
            return data
        email_check = Instructors.objects.filter(email=data).exists()
        if not email_check:
            return data
        raise Exception("Email already exists")
    
    def validate_phone(self,data):
        instance = self.instance
        if instance is not None and instance.phone == data:
            return data
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
    
    def update(self,instance,validated_data):

        courses_taught_data = validated_data.pop("courses_taught", [])
        existing_courses_ids = [course.id for course in instance.courses_taught.all()]

        for course_data in courses_taught_data:
            course, created = Courses.objects.get_or_create(**course_data)
            if course.id not in existing_courses_ids:
                instance.courses_taught.add(course)


        instance.name =  validated_data.get('name',instance.name)
        instance.email =  validated_data.get('email',instance.email)
        instance.phone =  validated_data.get('phone',instance.phone)
        instance.password =  validated_data.get('password',instance.password)
        instance.country =  validated_data.get('country',instance.country)
        instance.address =  validated_data.get('address',instance.address)
        instance.zipcode =  validated_data.get('zipcode',instance.zipcode)
        instance.profile_image =  validated_data.get('profile_image',instance.profile_image)
        instance.total_reviews =  validated_data.get('total_reviews',instance.total_reviews)
        instance.save()
        return instance

