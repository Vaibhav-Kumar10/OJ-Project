from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Problem, Submission


# ----------------- Home Page ----------------- #
def home_view(request):
    featured_problems = Problem.objects.filter(is_complete=True).order_by("-score")[:4]
    return render(request, "core/home.html", {"featured_problems": featured_problems})


# ----------------- List All Problems ----------------- #
def all_problems_view(request):
    problems = Problem.objects.all()
    return render(request, "core/allproblems.html", {"problems": problems})


# ----------------- Problem Detail View ----------------- #
@login_required
def problem_view(request, id):
    problem = get_object_or_404(Problem, id=id)
    user_submissions = Submission.objects.filter(
        user=request.user, problem=problem
    ).order_by("-submitted_at")
    context = {
        "problem": problem,
        "submissions": user_submissions,
    }
    return render(request, "core/problem_detail.html", context=context)
