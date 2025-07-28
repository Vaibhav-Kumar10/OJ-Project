from django.shortcuts import render
from .models import UserScore


def leaderboard_view(request):
    scores = UserScore.objects.select_related("user").order_by("-score", "-problems_solved")

    context = {"scores": scores}

    return render(request, "contests/leaderboard.html", context=context)


def contests_view(request):
    return render(request, "contests/contests.html")
