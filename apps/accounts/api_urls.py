from django.urls import path

from .api_views import StudentLoginAPIView

urlpatterns = [

    path(
        "student-login/",
        StudentLoginAPIView.as_view(),
        name="student_login_api"
    ),

]