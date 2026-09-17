from apps.prediction.models import Alert
from apps.students.models import Student
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):

    if request.user.role != "admin":

        return Response(
            {
                "success": False,
                "message": "Access denied"
            },
            status=403
        )

    students = Student.objects.all()

    total_students = students.count()

    high_risk = students.filter(
        risk_level="High"
    ).count()

    medium_risk = students.filter(
        risk_level="Medium"
    ).count()

    low_risk = students.filter(
        risk_level="Low"
    ).count()

    recent_alerts = Alert.objects.order_by(
        "-created_at"
    )[:5]

    alerts = []

    for alert in recent_alerts:

        alerts.append({

            "student": alert.student.name,

            "message": alert.message,

            "created_at": alert.created_at.strftime(
                "%d-%m-%Y %H:%M"
            )

        })

    return Response({

        "success": True,

        "admin":{

            "username":request.user.username,

            "email":request.user.email

        },

        "dashboard":{

            "total_students":total_students,

            "high_risk":high_risk,

            "medium_risk":medium_risk,

            "low_risk":low_risk

        },

        "recent_alerts":alerts

    })



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def student_dashboard(request):

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:

        return Response(
            {
                "success": False,
                "message": "Student not found"
            },
            status=404
        )

    return Response({

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

        }

    })
