from django.urls import path
from .views import (
    home_view,
    all_problems_view,
    problem_view,
    dashboard_view,
    get_ai_review,
)

app_name = "core"
urlpatterns = [
    path("", home_view, name="home"),
    path("problems/", all_problems_view, name="problems"),
    path("problem/<int:id>/", problem_view, name="problem_detail"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("ai_review/", get_ai_review, name="ai_review"),
    # path("submit/", submit_solution, name="submit"),
    # path("run/", run_code, name="run"),
]
