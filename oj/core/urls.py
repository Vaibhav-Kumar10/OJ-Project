from django.urls import path
from .views import home_view, all_problems_view, problem_view

app_name = "core"
urlpatterns = [
    path("", home_view, name="home"),
    path("problems/", all_problems_view, name="problems"),
    path("problem/<int:id>/", problem_view, name="problem_detail"),
    # path("submit/", submit_solution, name="submit"),
    # path("run/", run_code, name="run"),
]
