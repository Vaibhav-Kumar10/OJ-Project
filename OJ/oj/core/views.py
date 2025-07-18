from django.shortcuts import render


# Create your views here.
def home(request):
    """
    Render the home page of the OJ application.
    """
    return render(request, "core/home.html")


def all_problems(request):
    """
    Render the list of problems available in the OJ application.
    """
    return render(request, "problems.html")
