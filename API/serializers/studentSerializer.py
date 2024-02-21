from rest_framework import serializers
from API.models.students import Students 
from API.models.courses import Courses
from .courseSerializer import CourseSerializer
from django.contrib.auth.hashers import make_password
import re


class StudentSerializer(serializers.ModelSerializer):
    courses_enrolled = CourseSerializer(many=True, required=False)

    class Meta:
        model = Students
        fields = '__all__'

    def validate_email(self,data):
        instance = self.instance
        if instance is not None and instance.email == data:
            return data
        
        email_check = Students.objects.filter(email=data).exists()
        if not email_check:
            return data
        raise Exception("Email already exists")
    
    def validate_phone(self,data):
        instance = self.instance
        if instance is not None and instance.phone == data:
            return data
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
    
    def update(self,instance,validated_data):

        courses_enrolled_data = validated_data.pop("courses_enrolled", [])
        existing_courses_ids = [course.id for course in instance.courses_enrolled.all()]

        for course_data in courses_enrolled_data:
            course, created = Courses.objects.get_or_create(**course_data)
            if course.id not in existing_courses_ids:
                instance.courses_enrolled.add(course)


        instance.name =  validated_data.get('name',instance.name)
        instance.email =  validated_data.get('email',instance.email)
        instance.phone =  validated_data.get('phone',instance.phone)
        instance.password =  validated_data.get('password',instance.password)
        instance.profileImage =  validated_data.get('profileImage',instance.profileImage)
        instance.billinginfo =  validated_data.get('billinginfo',instance.billinginfo)
        instance.subscription =  validated_data.get('subscription',instance.subscription)
        instance.fees_amount_paid =  validated_data.get('fees_amount_paid',instance.fees_amount_paid)
        instance.payment_method =  validated_data.get('payment_method',instance.payment_method)
        instance.wishlist = validated_data.get('wishlist',instance.wishlist)
        instance.save()
        return instance