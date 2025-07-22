from django.shortcuts import render


def leaderboard_view(request):
    return render(request, "contests/leaderboard.html")


def contests_view(request):
    return render(request, "contests/contests.html")
