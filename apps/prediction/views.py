# from django.shortcuts import render
from .models import Alert

from django.http import JsonResponse

def alerts_page(request):

    alerts = Alert.objects.select_related("student").order_by("-created_at")

    data = []

    for alert in alerts:

        data.append({

            "id": alert.id,

            "student": alert.student.name,

            "risk_level": alert.risk_level,

            "message": alert.message,

            "created_at": alert.created_at.strftime("%d-%m-%Y %H:%M")

        })

    return JsonResponse({

        "alerts": data

    })