from rest_framework import serializers
from .models import Course, CourseEnrollment
from users.models import User

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'invite_code', 'teacher', 'created_at']
        read_only_fields = ['invite_code', 'teacher', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['teacher'] = user
        return super().create(validated_data)

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ['id', 'course', 'student', 'student_username', 'joined_at']
        read_only_fields = ['joined_at']
