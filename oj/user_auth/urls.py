from django.urls import path
from .views import signup_view, login_view, logout_view, forgot_password_view, reset_password_view


app_name = "user_auth"

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("forgot-password/", forgot_password_view, name="forgot_password"),
    path("reset-password/<str:token>/", reset_password_view, name="reset_password"),
]
