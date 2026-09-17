from django.contrib import admin
from .models import (
    Student,
    StudentWellbeing
)


admin.site.register(
    Student
)


admin.site.register(
    StudentWellbeing
)