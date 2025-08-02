from django.db.models import Count, ExpressionWrapper, F, FloatField
from django.shortcuts import render
from .models import UserScore


def leaderboard_view(request):
    scores = (
        UserScore.objects.select_related("user")
        .annotate(
            total_submissions=Count("user__submission", distinct=True),
            accuracy=ExpressionWrapper(
                100.0 * F("problems_solved") / (F("user__submission__count") + 0.001),
                output_field=FloatField(),
            ),
        )
        .order_by("-score", "-problems_solved")
    )

    context = {"scores": scores}
    return render(request, "contests/leaderboard.html", context=context)


def contests_view(request):
    return render(request, "contests/contests.html")
