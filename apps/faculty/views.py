import random
from apps.students.models import Student
from django.shortcuts import get_object_or_404
from .models import CounsellingSession, Faculty
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.accounts.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication


@csrf_exempt
def faculty_register(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "POST request required"
            },
            status=405
        )

    try:

        data = json.loads(request.body)

        name = data.get("name")
        email = data.get("email")
        department = data.get("department")
        password = data.get("password")

        if Faculty.objects.filter(email=email).exists():
            return JsonResponse({
                "success": False,
                "message": "Faculty already exists"
            })

        faculty_id = "FC" + str(random.randint(100000, 999999))

        while Faculty.objects.filter(faculty_id=faculty_id).exists():
            faculty_id = "FC" + str(random.randint(100000, 999999))

        user = User.objects.create_user(
            username=faculty_id,
            email=email,
            password=password,
            role="admin"      # we'll improve this later
        )

        Faculty.objects.create(
            user=user,
            faculty_id=faculty_id,
            name=name,
            email=email,
            department=department,
            password=password,
            is_approved=False
        )

        return JsonResponse({
            "success": True,
            "message": "Faculty Registration Successful",
            "faculty_id": faculty_id
        })

    except Exception as e:

        return JsonResponse(
            {
                "success": False,
                "message": str(e)
            },
            status=500
        )
@api_view(["POST"])
def faculty_login(request):

    faculty_id = request.data.get("faculty_id")
    password = request.data.get("password")

    try:
        faculty = Faculty.objects.get(faculty_id=faculty_id)

    except Faculty.DoesNotExist:

        return Response({
            "success": False,
            "message": "Faculty not found"
        }, status=404)

    if faculty.password != password:

        return Response({
            "success": False,
            "message": "Invalid password"
        }, status=400)

    user = faculty.user

    refresh = RefreshToken.for_user(user)

    return Response({

        "success": True,

        "access": str(refresh.access_token),

        "refresh": str(refresh),

        "faculty": {

            "id": faculty.id,

            "name": faculty.name,

            "faculty_id": faculty.faculty_id,

            "email": faculty.email,

            "department": faculty.department

        }

    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def faculty_dashboard(request):

    try:

        faculty = Faculty.objects.get(user=request.user)

    except Faculty.DoesNotExist:

        return Response(
            {
                "success": False,
                "message": "Faculty not found"
            },
            status=404
        )

    total_students = Student.objects.count()

    high_risk_students = Student.objects.filter(
        risk_level="High"
    )

    medium_risk_students = Student.objects.filter(
        risk_level="Medium"
    )

    low_risk_students = Student.objects.filter(
        risk_level="Low"
    )

    counselling_count = CounsellingSession.objects.count()

    return Response({

        "success": True,

        "faculty": {

            "id": faculty.id,
            "name": faculty.name,
            "faculty_id": faculty.faculty_id,
            "email": faculty.email,
            "department": faculty.department

        },

        "dashboard": {

            "total_students": total_students,

            "high_risk_count": high_risk_students.count(),

            "medium_risk_count": medium_risk_students.count(),

            "low_risk_count": low_risk_students.count(),

            "counselling_count": counselling_count

        },

        "students": [

            {

                "id": s.id,

                "name": s.name,

                "register_number": s.register_number,

                "attendance": s.attendance,

                "marks": s.marks,

                "risk_level": s.risk_level

            }

            for s in Student.objects.exclude(
                risk_level="Low"
            )

        ]

    })


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def faculty_students(request):

    students = Student.objects.all()

    data = []

    for student in students:

        data.append({

            "id": student.id,

            "name": student.name,

            "register_number": student.register_number,

            "attendance": student.attendance,

            "marks": student.marks,

            "discipline": student.discipline,

            "risk_level": student.risk_level

        })

    return JsonResponse({

        "students": data

    })



@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_student_academics(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    if request.method == "GET":

        return JsonResponse({

            "student": {

                "id": student.id,

                "name": student.name,

                "register_number": student.register_number,

                "attendance": student.attendance,

                "marks": student.marks,

                "discipline": student.discipline,

                "risk_level": student.risk_level

            }

        })

    data = request.data

    student.attendance = int(data.get("attendance", 0))
    student.marks = int(data.get("marks", 0))
    student.discipline = int(data.get("discipline", 0))

    if (
        student.attendance < 50 or
        student.marks < 40 or
        student.discipline < 40
    ):
        student.risk_level = "High"

    elif (
        student.attendance < 70 or
        student.marks < 60 or
        student.discipline < 60
    ):
        student.risk_level = "Medium"

    else:
        student.risk_level = "Low"

    student.save()

    return JsonResponse({

        "success": True,

        "message": "Academic details updated successfully.",

        "risk_level": student.risk_level

    })


@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def counselling_page(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "GET":

        sessions = CounsellingSession.objects.filter(
            student=student
        ).order_by("-created_at")

        return JsonResponse({

            "student": {

                "id": student.id,
                "name": student.name,
                "register_number": student.register_number

            },

            "sessions": [

                {

                    "faculty_name": session.faculty_name,
                    "message": session.message,
                    "created_at": session.created_at.isoformat()

                }

                for session in sessions

            ]

        })

    if request.method == "POST":

        data = json.loads(request.body)

        faculty_name = (
            request.user.get_full_name()
            or request.user.username
        )

        session = CounsellingSession.objects.create(

            student=student,

            faculty_name=faculty_name,

            message=data["message"]

        )

        return JsonResponse({

            "success": True,

            "message": "Counselling advice sent successfully.",

            "session": {

                "faculty_name": session.faculty_name,
                "message": session.message,
                "created_at": session.created_at.isoformat()

            }

        })



def faculty_list(request):

    faculties = Faculty.objects.all()

    data = []

    for faculty in faculties:
        data.append({
            "id": faculty.id,
            "name": faculty.name,
            "faculty_id": faculty.faculty_id,
            "department": faculty.department,
            "email": faculty.email,
        })

    return JsonResponse({
        "faculties": data
    })




@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_faculty(request, faculty_id):

    try:

        faculty = Faculty.objects.get(id=faculty_id)

        faculty.delete()

        return JsonResponse({

            "success": True,

            "message": "Faculty deleted successfully"

        })

    except Faculty.DoesNotExist:

        return JsonResponse({

            "success": False,

            "message": "Faculty not found"

        }, status=404)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def faculty_insight(request, faculty_id):

    try:

        faculty = Faculty.objects.get(id=faculty_id)

    except Faculty.DoesNotExist:

        return JsonResponse({

            "success": False,
            "message": "Faculty not found"

        }, status=404)

    counselling_sessions = CounsellingSession.objects.filter(
        faculty_name=faculty.name
    )

    sessions = []

    for session in counselling_sessions:

        sessions.append({

            "student_name": session.student_name,
            "date": str(session.date),
            "status": session.status

        })

    return JsonResponse({

        "success": True,

        "faculty": {

            "id": faculty.id,
            "name": faculty.name,
            "faculty_id": faculty.faculty_id,
            "department": faculty.department,
            "email": faculty.email

        },

        "sessions": sessions

    })
