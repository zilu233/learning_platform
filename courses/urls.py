from django.urls import path
from .views import CourseCreateView, JoinCourseView, CourseStudentsView

urlpatterns = [
    path('', CourseCreateView.as_view(), name='teacher-courses'),            # 教师查看/创建课程
    path('join/', JoinCourseView.as_view(), name='join-course'),             # 学生加入课程
    path('<int:course_id>/students/', CourseStudentsView.as_view(), name='course-students'),  # 查看选课学生
]
