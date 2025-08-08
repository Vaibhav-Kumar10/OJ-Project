from django.db.models import Count, ExpressionWrapper, F, FloatField
from django.db.models import Count, Sum, F, FloatField, ExpressionWrapper, Q
from django.shortcuts import render
from .models import UserScore
from core.models import Problem
from .models import UserScore
from django.contrib.auth import get_user_model


from core.models import Submission
User = get_user_model()

def leaderboard_view(request):
    users_with_scores = (
        User.objects.annotate(
            problems_solved=Count(
                "submission", filter=Q(submission__verdict="Accepted"), distinct=True
            ),
            total_submissions=Count("submission", distinct=True),
            score=Sum(
                "submission__problem__score", filter=Q(submission__verdict="Accepted")
            ),
        )
        .annotate(
            accuracy=ExpressionWrapper(
                100.0 * F("problems_solved") / (F("total_submissions") + 0.001),
                output_field=FloatField(),
            )
        )
        .filter(problems_solved__gt=0)  # only users who solved something
        .order_by("-score", "-problems_solved")
    )

    context = {"scores": users_with_scores}
    return render(request, "contests/leaderboard.html", context)



def contests_view(request):
    return render(request, "contests/contests.html")
