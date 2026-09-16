from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from account.serializers import (
    RegisterSerializer,
    LoginSerializer,
)
from account.services import (
    register_user,
    login_user,
    logout_user,
    refresh_user_token
)


# signup views
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


# login views
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
                },
                "tokens": {
                    "access_token": str(access_token),
                    "refresh_token": str(refresh),
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


# logout views
class LogoutView(APIView):

    permission_classes = []

    def post(self, request):

        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            logout_user(
                refresh_token=refresh_token
            )

        response = Response(
            {
                "message": "Logout successful."
            },
            status=status.HTTP_200_OK
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response


# user details
class MeView(APIView):

    def get(self, request):

        user = request.user

        return Response({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email
        }, status=status.HTTP_200_OK)


# refresh token 
class RefreshView(APIView):
     
    permission_classes = []

    def post(self, request):

   
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {
                    "detail": "Refresh token not found."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
     
            access_token, new_refresh = refresh_user_token(
                refresh_token=refresh_token
            )

        except Exception:
            return Response(
                {
                    "detail": "Invalid or expired refresh token."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response(
            {
                "message": "Token refreshed successfully."
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
            value=str(new_refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return response
