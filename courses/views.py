from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, CourseEnrollment
from .serializers import CourseSerializer, CourseEnrollmentSerializer
from users.models import User

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class CourseCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class JoinCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        code = request.data.get('invite_code')
        try:
            course = Course.objects.get(invite_code=code)
        except Course.DoesNotExist:
            return Response({'error': 'Invalid invite code'}, status=400)

        enrollment, created = CourseEnrollment.objects.get_or_create(course=course, student=request.user)
        if not created:
            return Response({'message': 'Already enrolled'}, status=200)

        return Response({'message': 'Successfully joined course'})

class CourseStudentsView(generics.ListAPIView):
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return CourseEnrollment.objects.filter(course__id=course_id, course__teacher=self.request.user)
