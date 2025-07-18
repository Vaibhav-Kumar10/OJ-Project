from django.shortcuts import render

# Create your views here.


def login(request):
    """
    Render the login page of the OJ application.
    """
    return render(request, "login.html")


def signup(request):
    """
    Render the signup page of the OJ application.
    """
    return render(request, "signup.html")


def dashboard(request):
    """
    Render the dashboard page of the OJ application.
    """
    return render(request, "dashboard.html")
