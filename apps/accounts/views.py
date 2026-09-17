from apps.faculty.models import Faculty
from apps.students.models import Student
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

def landing_page(request):

    return redirect("http://localhost:4200/")


@api_view(["POST"])
def admin_login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is None or user.role != "admin":

        return Response(
            {
                "success": False,
                "message": "Invalid admin credentials"
            },
            status=401
        )

    refresh = RefreshToken.for_user(user)

    return Response({

        "success": True,

        "access": str(refresh.access_token),

        "refresh": str(refresh),

        "admin": {

            "id": user.id,

            "username": user.username,

            "email": user.email,

            "role": user.role

        }

    })

@api_view(["POST"])
def faculty_login(request):

    faculty_id = request.data.get("faculty_id")
    password = request.data.get("password")

    try:
        faculty = Faculty.objects.get(faculty_id=faculty_id)

    except Faculty.DoesNotExist:
        return Response({
            "success": False,
            "message": "Invalid Faculty ID"
        })

    if not faculty.is_approved:
        return Response({
            "success": False,
            "message": "Waiting for admin approval"
        })

    user = faculty.user

    if not user.check_password(password):
        return Response({
            "success": False,
            "message": "Invalid Password"
        })

    refresh = RefreshToken.for_user(user)

    return Response({

        "success": True,

        "access": str(refresh.access_token),

        "refresh": str(refresh),

        "faculty": {

            "id": faculty.id,

            "faculty_id": faculty.faculty_id,

            "name": faculty.name,

            "email": faculty.email,

            "department": faculty.department

        }

    })



@csrf_exempt
def student_login(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "POST request required"
            },
            status=405
        )

    register_number = request.POST.get("register_number")
    password = request.POST.get("password")

    user = authenticate(
        request,
        username=register_number,
        password=password
    )

    if user is None:
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid credentials"
            },
            status=401
        )

    try:
        student = Student.objects.get(user=user)

    except Student.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "message": "Student record not found"
            },
            status=404
        )

    if not student.is_approved:
        return JsonResponse(
            {
                "success": False,
                "message": "Waiting for admin approval"
            },
            status=403
        )

    login(request, user)

    return JsonResponse(
        {
            "success": True,
            "message": "Login Successful",
            "student": {
                "id": student.id,
                "name": student.name,
                "register_number": student.register_number
            }
        }
    )

