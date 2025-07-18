from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("problems/", views.all_problems, name="all_problems"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("contests/", views.contest, name="contests"),
    path("dashboard/", views.contest, name="dashboard"),
]
