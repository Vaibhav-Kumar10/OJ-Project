from django.urls import path
from .views import run_code_api

urlpatterns = [
    path("run/", run_code_api, name="run_code_api"),
]
