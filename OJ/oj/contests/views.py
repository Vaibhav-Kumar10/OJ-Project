from django.shortcuts import render

# Create your views here.

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