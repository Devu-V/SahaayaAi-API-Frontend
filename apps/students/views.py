from .models import Student
from .models import StudentWellbeing
from apps.faculty.models import CounsellingSession
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes


def students_list(request):

    students = Student.objects.all()

    data = []

    for student in students:

        data.append({

            "id": student.id,
            "name": student.name,
            "register_number": student.register_number,
            "risk_level": student.risk_level

        })

    return JsonResponse({

        "students": data

    })


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_student(request, student_id):

    try:

        student = Student.objects.get(id=student_id)

        student.delete()

        return JsonResponse({

            "success": True,
            "message": "Student deleted successfully"

        })

    except Student.DoesNotExist:

        return JsonResponse({

            "success": False,
            "message": "Student not found"

        }, status=404)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def student_profile(request):

    try:

        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "message": "Student profile not found"
            },
            status=404
        )


    wellbeing, created = StudentWellbeing.objects.get_or_create(
        student=student
    )


    counselling_messages = CounsellingSession.objects.filter(
        student=student
    ).order_by("-created_at")


    messages_data = []

    for msg in counselling_messages:

        messages_data.append(
            {
                "faculty_name": msg.faculty_name,
                "message": msg.message,
                "created_at": msg.created_at
            }
        )


    return JsonResponse(
        {
            "success": True,

            "student": {

                "id": student.id,

                "name": student.name,

                "register_number": student.register_number,

                "email": student.email,

                "attendance": student.attendance,

                "marks": student.marks,

                "discipline": student.discipline,

                "risk_level": student.risk_level,

                "risk_score": student.risk_score,

                "risk_reason": student.risk_reason,

                "ai_recommendation": student.ai_recommendation

            },


            "wellbeing": {

                "stress_level": wellbeing.stress_level,

                "sleep_quality": wellbeing.sleep_quality,

                "social_activity": wellbeing.social_activity,

                "motivation_level": wellbeing.motivation_level,

                "mood": wellbeing.mood,

                "updated_at": wellbeing.updated_at

            },


            "counselling_messages": messages_data

        }
    )


@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def wellbeing_form(request):

    student = Student.objects.get(user=request.user)

    wellbeing, created = StudentWellbeing.objects.get_or_create(
        student=student
    )

    if request.method == "GET":

        return JsonResponse({

            "stress_level": wellbeing.stress_level,
            "sleep_quality": wellbeing.sleep_quality,
            "social_activity": wellbeing.social_activity,
            "motivation_level": wellbeing.motivation_level,
            "mood": wellbeing.mood

        })

    import json
    data = json.loads(request.body)

    wellbeing.stress_level = data["stress_level"]
    wellbeing.sleep_quality = data["sleep_quality"]
    wellbeing.social_activity = data["social_activity"]
    wellbeing.motivation_level = data["motivation_level"]
    wellbeing.mood = data["mood"]

    wellbeing.save()

    from apps.prediction.utils import calculate_risk

    risk = calculate_risk(student, wellbeing)

    return JsonResponse({

        "success": True,
        "risk_level": risk,
        "message": "Wellbeing data saved successfully."

    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def student_insight(request, student_id):

    try:

        student = Student.objects.get(id=student_id)

    except Student.DoesNotExist:

        return JsonResponse({

            "success": False,
            "message": "Student not found"

        }, status=404)

    wellbeing = StudentWellbeing.objects.filter(
        student=student
    ).first()

    return JsonResponse({

        "success": True,

        "student": {

            "id": student.id,
            "name": student.name,
            "register_number": student.register_number,
            "email": student.email,
            "attendance": student.attendance,
            "marks": student.marks,
            "discipline": student.discipline,
            "risk_level": student.risk_level,
            "risk_score": student.risk_score,
            "risk_reason": student.risk_reason,
            "ai_recommendation": student.ai_recommendation

        },

        "wellbeing": {

            "sleep_hours": wellbeing.sleep_hours if wellbeing else None,
            "stress_level": wellbeing.stress_level if wellbeing else None,
            "financial_stress": wellbeing.financial_stress if wellbeing else None,
            "family_support": wellbeing.family_support if wellbeing else None,
            "social_activity": wellbeing.social_activity if wellbeing else None

        }

    })


User = get_user_model()

@csrf_exempt
def student_register(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "Only POST method is allowed"
            },
            status=405
        )

    try:

        data = json.loads(request.body)

        name = data.get("name")
        register_number = data.get("register_number")
        email = data.get("email")
        password = data.get("password")

        if not all([name, register_number, email, password]):
            return JsonResponse(
                {
                    "success": False,
                    "message": "All fields are required"
                },
                status=400
            )

        if Student.objects.filter(register_number=register_number).exists():
            return JsonResponse(
                {
                    "success": False,
                    "message": "Register number already exists"
                },
                status=400
            )

        if User.objects.filter(username=register_number).exists():
            return JsonResponse(
                {
                    "success": False,
                    "message": "User already exists"
                },
                status=400
            )

        approved = (
            register_number.startswith("ST")
            and len(password) >= 6
        )

        with transaction.atomic():

            user = User.objects.create_user(
                username=register_number,
                email=email,
                password=password,
                role="student"
            )

            Student.objects.create(
                user=user,
                name=name,
                register_number=register_number,
                email=email,

                # Temporary (will remove later)
                password=password,

                attendance=0,
                marks=0,
                discipline=0,

                risk_level="Low",
                risk_score=0,

                is_approved=approved
            )

        return JsonResponse(
            {
                "success": True,
                "message": (
                    "Student verified and approved successfully"
                    if approved
                    else "Registration submitted for admin approval"
                )
            }
        )

    except Exception as e:

        return JsonResponse(
            {
                "success": False,
                "message": str(e)
            },
            status=500
        )