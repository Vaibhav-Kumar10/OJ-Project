from django.shortcuts import render


def login_view(request):
    return render(request, "auth/login.html")


def signup_view(request):
    """
    Render the signup page of the OJ application.
    """
    return render(request, "auth/signup.html")


def dashboard_view(request):
    """
    Render the dashboard page of the OJ application.
    """
    return render(request, "auth/dashboard.html")


def logout_view(request):
    """
    Handle user logout in the OJ application.
    """
    from django.contrib.auth import logout

    logout(request)
    return render(request, "logout.html")
