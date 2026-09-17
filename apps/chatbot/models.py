from django.db import models
from apps.students.models import Student

class ChatMessage(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE)

    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.created_at}"