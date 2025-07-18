from django.urls import path
from . import views

app_name = "compiler"

urlpatterns = [
    path("submit/", views.submit_code, name="submit_code"),
]
