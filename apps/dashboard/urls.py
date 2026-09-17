from django.urls import path
from .views import (
    admin_dashboard,
    student_dashboard

)

urlpatterns = [
    path(
        'admin/',
        admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'student/',
        student_dashboard,
        name='student_dashboard'
    ),
    
]