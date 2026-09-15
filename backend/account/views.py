from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import (
    RegisterSerializer,
    LoginSerializer,
)
from account.services import (
    register_user,
    login_user,
)


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Make a copy of validated_data and remove confirm_password
        validated_data = serializer.validated_data.copy()
        validated_data.pop("confirm_password", None)

        user = register_user(**validated_data)

        return Response(
            {
                "message": "User registered successfully.",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                }
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:
            user, refresh = login_user(
                **serializer.validated_data
            )

        except ValueError as error:
            return Response(
                {
                    "detail": str(error)
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = refresh.access_token

        response = Response(
            {
                "message": "Login successful.",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                }
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=str(access_token),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=15 * 60,
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return response
