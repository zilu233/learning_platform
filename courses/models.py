from django.db import models
from users.models import User
import uuid

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    invite_code = models.CharField(max_length=10, unique=True, default=uuid.uuid4().hex[:10])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')
