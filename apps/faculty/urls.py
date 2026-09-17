from django.urls import path


from .views import (
    faculty_register,
    faculty_login,
    faculty_dashboard,
    faculty_students,
    update_student_academics,
    counselling_page
)

urlpatterns = [

    path(
        'faculty-register/',
        faculty_register
    ),

    path(
        'faculty-login/',
        faculty_login
    ),

    path(
        'faculty-dashboard/',
        faculty_dashboard
    ),

    path(
    'faculty-students/',
    faculty_students
),

path(
    'update-student-academics/<int:student_id>/',
    update_student_academics
),

path(
    'counselling/<int:student_id>/',
    counselling_page
),
]