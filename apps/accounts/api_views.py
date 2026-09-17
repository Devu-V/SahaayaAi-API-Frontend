from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from apps.students.models import Student

from .serializers import LoginSerializer


class StudentLoginAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        register_number = serializer.validated_data["register_number"]
        password = serializer.validated_data["password"]

        user = authenticate(
            username=register_number,
            password=password
        )

        if user is None:

            return Response(
                {
                    "success": False,
                    "message": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:

            student = Student.objects.get(user=user)

        except Student.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Student record not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not student.is_approved:

            return Response(
                {
                    "success": False,
                    "message": "Waiting for admin approval"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)

        return Response({

            "success": True,

            "access": str(refresh.access_token),

            "refresh": str(refresh),

            "student": {

                "id": student.id,

                "name": student.name,

                "register_number": student.register_number,

                "email": student.email,

                "risk_level": student.risk_level

            }

        })