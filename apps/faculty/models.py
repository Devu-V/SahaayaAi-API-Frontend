from django.db import models

from apps.students.models import Student
from apps.accounts.models import User


class Faculty(models.Model):

    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    faculty_id = models.CharField(
        max_length=20
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    department = models.CharField(
        max_length=100
    )

    password = models.CharField(
        max_length=100
    )

    is_approved = models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.name


class CounsellingSession(models.Model):

    student = models.ForeignKey(

        Student,

        on_delete=models.CASCADE
    )

    faculty_name = models.CharField(
        max_length=100
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.student.name