from django.http import JsonResponse
from groq import Groq
from .models import ChatMessage
from apps.students.models import Student

from dotenv import load_dotenv
import os
import json


from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes
)

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)




@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def chatbot(request):


    try:

        student = Student.objects.get(
            user=request.user
        )


    except Student.DoesNotExist:


        return JsonResponse(
            {
                "success":False,
                "message":"Student not found"
            },
            status=404
        )


    if request.method == "GET":


        chats = ChatMessage.objects.filter(

            student=student

        ).order_by(
            "created_at"
        )


        data=[]

        for chat in chats:

            data.append({

                "user_message":
                chat.user_message,


                "bot_response":
                chat.bot_response,


                "created_at":
                chat.created_at

            })

        return JsonResponse({

            "success":True,

            "chats":data

        })

    data=json.loads(
        request.body
    )

    user_message=data.get(
        "message"
    )

    if not user_message:

        return JsonResponse({

            "success":False,

            "message":
            "Message required"

        },status=400)


    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",

                "content":
                """
                You are Sahaaya AI,
                a supportive student mental
                wellness assistant.

                Help students with:
                stress,
                motivation,
                academics,
                sleep,
                emotional support.

                Be friendly and concise.
                """
            },


            {
                "role":"user",

                "content":
                user_message
            }
        ]

    )

    bot_response = (
        completion
        .choices[0]
        .message
        .content
    )

    ChatMessage.objects.create(

        student=student,

        user_message=user_message,

        bot_response=bot_response

    )

    return JsonResponse({

        "success":True,

        "reply":bot_response

    })