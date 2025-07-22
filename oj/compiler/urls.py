from django.urls import path
from .views import run_code_view

app_name = "compiler"

urlpatterns = [
    path("run/", run_code_view, name="run_code"),
]
