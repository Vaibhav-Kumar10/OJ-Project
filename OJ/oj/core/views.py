from django.shortcuts import render


# Create your views here.
def home(request):
    """
    Render the home page of the OJ application.
    """
    return render(request, "home.html")


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


def all_problems(request):
    """
    Render the list of problems available in the OJ application.
    """
    return render(request, "problems.html")


def leaderboard(request):
    """
    Render the leaderboard page of the OJ application.
    """
    return render(request, "leaderboard.html")


def contest(request):
    """
    Render the contest page of the OJ application.
    """
    return render(request, "contests.html")

def dashboard(request):
    """
    Render the dashboard page of the OJ application.
    """
    return render(request, "dashboard.html")
