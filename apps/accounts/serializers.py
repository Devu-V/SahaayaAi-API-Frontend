from rest_framework import serializers


class LoginSerializer(serializers.Serializer):

    register_number = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )