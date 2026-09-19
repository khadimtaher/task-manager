import re
from rest_framework import serializers

# Signup
class RegisterSerializer(serializers.Serializer):  

    full_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8  # Min length 8 update kar di gayi hai
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate_email(self, value):
        from account.models import User

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exist"
            )

        return value.lower()

    def validate(self, data):
        # 1. Password match check
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError({
                "confirm_password": "Password do not match"
            })

        # 2. Custom Password Strength Validation (Frontend match)
        password = data.get("password")
        if password:
            if len(password) < 8:
                raise serializers.ValidationError({
                    "password": "Password must be at least 8 characters long."
                })
            if not re.search(r'[A-Z]', password):
                raise serializers.ValidationError({
                    "password": "Password must contain at least one uppercase letter."
                })
            if not re.search(r'[a-z]', password):
                raise serializers.ValidationError({
                    "password": "Password must contain at least one lowercase letter."
                })
            if not re.search(r'[0-9]', password):
                raise serializers.ValidationError({
                    "password": "Password must contain at least one number."
                })

        return data

# login


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True
    )
