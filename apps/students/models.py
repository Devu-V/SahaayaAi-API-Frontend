from django.db import models
from django.conf import settings

class Student(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    register_number = models.CharField(
        max_length=100,
        unique=True
    )

    password = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    attendance = models.IntegerField(
        default=0
    )

    marks = models.IntegerField(
        default=0
    )

    discipline = models.IntegerField(
        default=0
    )

    risk_level = models.CharField(
        max_length=20,
        default='Low'
    )

    risk_score = models.FloatField(
        default=0
    )

    risk_reason = models.TextField(
        blank=True,
        null=True
    )

    ai_recommendation = models.TextField(
        blank=True,
        null=True
    )

    is_approved = models.BooleanField(
    default=False
)

    created_at = models.DateTimeField(
    auto_now_add=True,
    null=True,
    blank=True
)

    email = models.EmailField(
    null=True,
    blank=True
)

    def __str__(self):

        return self.name


class StudentWellbeing(models.Model):

    student = models.OneToOneField(

        Student,

        on_delete=models.CASCADE
    )

    stress_level = models.IntegerField(
        default=5
    )

    sleep_quality = models.IntegerField(
        default=5
    )

    social_activity = models.IntegerField(
        default=5
    )

    motivation_level = models.IntegerField(
        default=5
    )

    mood = models.CharField(

        max_length=20,

        default='Neutral'
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.student.name


