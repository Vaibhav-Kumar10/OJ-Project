from django.urls import path
from .views import run_code_view, submit_code_view, quick_run_view

app_name = "compiler"

urlpatterns = [
    path("run/", run_code_view, name="run_code"),
    path("submit/", submit_code_view, name="submit_code"),
    path("quick-run/", quick_run_view, name="quick_run"),
]
