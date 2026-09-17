from django.db import models
from apps.students.models import Student


class Alert(models.Model):

    RISK_LEVEL_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low')
    ]

    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('READ', 'Read'),
        ('RESOLVED', 'Resolved')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    message = models.TextField()

    risk_level = models.CharField(
        max_length=10,
        choices=RISK_LEVEL_CHOICES
    )

    risk_score = models.FloatField(default=0)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='NEW'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.risk_level}"