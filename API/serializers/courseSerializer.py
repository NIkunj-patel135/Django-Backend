from rest_framework import serializers
from API.models.courses import Courses
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
 