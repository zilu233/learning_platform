from django.db import models
from courses.models import Course
from users.models import User

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    auto_grading = models.BooleanField(default=False)  # 是否自动批改
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assignment', 'student')

class Question(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='questions')
    QUESTION_TYPES = (
        ('choice', '选择题'),
        ('code', '编程题'),
    )
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    content = models.TextField()
    correct_answer = models.CharField(max_length=200, blank=True, null=True)  # 对于选择题
    score = models.FloatField(default=5.0)

    def __str__(self):
        return f"{self.assignment.title} - {self.content[:30]}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class CodeTestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()

class QuestionSubmission(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='question_submissions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    result = models.CharField(max_length=50, default='pending')  # correct / wrong / error
    score = models.FloatField(default=0)
