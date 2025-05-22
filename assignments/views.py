from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Assignment, Submission, QuestionSubmission, Question
from .serializers import AssignmentSerializer, SubmissionSerializer
from users.models import User
from courses.models import Course
from .grading import grade_choice_question, grade_code_question


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

# 教师发布作业
class AssignmentCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Assignment.objects.filter(course__teacher=self.request.user)

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        course = Course.objects.get(id=course_id)
        if course.teacher != self.request.user:
            raise PermissionError("You can only create assignments for your own courses")
        serializer.save()

# 学生查看课程作业
class CourseAssignmentsView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Assignment.objects.filter(course__id=course_id)

# 学生提交作业
class SubmitAssignmentView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        assignment = Assignment.objects.get(id=self.request.data.get('assignment'))
        submission = serializer.save(student=self.request.user, assignment=assignment)

        # 简单自动批改示例：若关键词“正确”在答案中则得满分
        if assignment.auto_grading:
            if "正确" in (submission.answer_text or ""):
                submission.score = 100
            else:
                submission.score = 0
            submission.save()

# 教师查看某作业的提交列表
class AssignmentSubmissionsView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        return Submission.objects.filter(assignment__id=assignment_id, assignment__course__teacher=self.request.user)

def perform_create(self, serializer):
    assignment = Assignment.objects.get(id=self.request.data.get('assignment'))
    submission = serializer.save(student=self.request.user, assignment=assignment)

    # 解析每个题目的答案
    answers = self.request.data.get('answers', [])  # [{question_id, answer}]
    total_score = 0

    for ans in answers:
        qid = ans['question_id']
        content = ans['answer']
        question = Question.objects.get(id=qid)
        q_submission = QuestionSubmission.objects.create(
            submission=submission,
            question=question,
            answer=content
        )

        if question.question_type == 'choice':
            grade_choice_question(q_submission)
        elif question.question_type == 'code':
            grade_code_question(q_submission)

        total_score += q_submission.score

    submission.score = total_score
    submission.save()