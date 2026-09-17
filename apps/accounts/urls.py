from django.urls import path

from .views import (
    landing_page,
    admin_login,
    student_login
)

urlpatterns = [
    path('', landing_page,name='landing_page'),
    path('admin-login/',admin_login,name='admin_login'),
    path( 'student-login/', student_login, name='student_login'),
]