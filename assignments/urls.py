from django.urls import path
from .views import (
    AssignmentCreateView,
    CourseAssignmentsView,
    SubmitAssignmentView,
    AssignmentSubmissionsView,
)

urlpatterns = [
    path('', AssignmentCreateView.as_view(), name='create-assignment'),
    path('course/<int:course_id>/', CourseAssignmentsView.as_view(), name='course-assignments'),
    path('submit/', SubmitAssignmentView.as_view(), name='submit-assignment'),
    path('<int:assignment_id>/submissions/', AssignmentSubmissionsView.as_view(), name='assignment-submissions'),
]
