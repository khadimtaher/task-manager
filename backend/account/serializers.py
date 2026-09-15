from rest_framework import serializers

# Signup


class RegisterSerializer(serializers.Serializer):

    full_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, value):
        from account.models import User

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exist"
            )

        return value.lower()

    def validate(self, value):
        if value["password"] != value["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Password do not match"
            })

        return value

# login


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True
    )
