from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User

# signup 
def register_user(*, full_name, email, password):
    user = User.objects.create_user(
        email=email,
        password=password,
        full_name=full_name
    )

    return user


# login 
def login_user(*, email, password):
    user =authenticate(
        email=email,
        password=password
    )

    if not user:
        raise ValueError("Ivalid email or password")
    if not user.is_active:
        raise ValueError("User account is inactive")

    refresh = RefreshToken.for_user(user)
    return user, refresh

# logout

def logout_user(*, refresh_token):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        pass
