from django.contrib import admin
from django.urls import path,include

from apps.accounts.views import (
    landing_page,
    admin_login,
    student_login,
   
    
)

from apps.dashboard.views import (
    admin_dashboard,
    student_dashboard,

)

from apps.students.views import (
 
    delete_student,
    wellbeing_form,
    student_profile,
    student_insight,
    student_register,
    students_list
)

from apps.chatbot.views import (
    chatbot
)
from apps.prediction.views import alerts_page

from apps.faculty.views import (
    update_student_academics,
    faculty_insight,
    delete_faculty,
    faculty_list
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path(
    "api/token/",
    TokenObtainPairView.as_view(),
    name="token_obtain_pair",
),

path(
    "api/token/refresh/",
    TokenRefreshView.as_view(),
    name="token_refresh",
),

path(
    "api/",
    include("apps.accounts.api_urls")
),

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        landing_page
    ),


    path(
        'admin-login/',
        admin_login
    ),

    path(
        'student-login/',
        student_login
    ),

    path(
        'student-register/',
        student_register
    ),

    path(
        'admin-dashboard/',
        admin_dashboard
    ),

    path(
    'students/',
    students_list
),

    path(
        'student-dashboard/',
        student_dashboard
    ),



    path(
        'students/delete/<int:student_id>/',
        delete_student
    ),
    path(
    'students/',
    include('apps.students.urls')
),

    path(
        'wellbeing-form/',
        wellbeing_form
    ),

    path(
        'student-profile/',
        student_profile
    ),
    path(
    'student-insight/<int:student_id>/',
    student_insight,
    name='student_insight'
),


  path(
    'chatbot/',
    chatbot
),
    
 path(
    'api/alerts/',
    alerts_page,
    name='alerts_page'
),

 path(
    '',
    include('apps.faculty.urls')
),

path('update-academics/<int:student_id>/',
    update_student_academics
      ),

path(
    'faculties/',
    faculty_list,
    name='faculty_list'
),

path(
    'faculty-delete/<int:faculty_id>/',
    delete_faculty,
    name='delete_faculty'
),

path(
    'faculty-insight/<int:faculty_id>/',
    faculty_insight,
    name='faculty_insight'
   )
]