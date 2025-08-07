from django.db.models import Count, ExpressionWrapper, F, FloatField
from django.shortcuts import render
from .models import UserScore
from core.models import Problem
from .models import UserScore


def leaderboard_view(request):
    scores = (
        UserScore.objects.select_related("user")
        .annotate(
            total_submissions=Count("user__submission", distinct=True),
            accuracy=ExpressionWrapper(
                100.0 * F("problems_solved") / (F("total_submissions") + 0.001),
                output_field=FloatField(),
            ),
        )
        .order_by("-score", "-problems_solved")
        .distinct("user")  # Ensures each user appears only once
    )
    context = {"scores": scores}
    return render(request, "contests/leaderboard.html", context=context)


def contests_view(request):
    return render(request, "contests/contests.html")
