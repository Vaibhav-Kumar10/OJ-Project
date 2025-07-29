from django.urls import path
from .views import (
    home_view,
    all_problems_view,
    problem_view,
    get_ai_review,
    profile_view,
)

app_name = "core"
urlpatterns = [
    path("", home_view, name="home"),
    path("problems/", all_problems_view, name="problems"),
    path("problem/<int:id>/", problem_view, name="problem_detail"),
    path("ai_review/", get_ai_review, name="ai_review"),
    path("profile/", profile_view, name="profile"),  # Current user's profile
    path("profile/<str:username>/", profile_view, name="user_profile"),  # Other user's profile
]
