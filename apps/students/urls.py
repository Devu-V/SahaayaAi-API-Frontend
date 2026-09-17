from django.urls import path
from .views import (

    students_list,
    delete_student,
    wellbeing_form,
    student_profile,
    student_insight,
    student_register
)

urlpatterns = [

    path(
        '',
        students_list
    ),

  

    path(
        'delete/<int:student_id>/',
        delete_student
    ),

   path(
    "wellbeing-form/",
    wellbeing_form,
    name="wellbeing_form"
),

    path(
    'student-profile/',
    student_profile,
    name="student_profile"
),

    path(
        'student-insight/<int:student_id>/',
        student_insight
    ),

    path(
    'student-register/',
    student_register
),

]