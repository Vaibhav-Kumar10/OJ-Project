from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Problem, Submission, TestCase


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


# ----------------- Submit Solution ----------------- #
@login_required
def submit_solution(request):
    if request.method == "POST":
        user = request.user
        problem_id = request.POST.get("problem_id")
        language = request.POST.get("language")
        code = request.POST.get("code")

        # # Validate inputs
        # if not problem_id or not language or not code:
        #     messages.error(request, "All fields are required.")
        #     return redirect("core:problems")

        # if not code.strip():
        #     messages.error(request, "Code cannot be empty.")
        #     return redirect("core:problems")

        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            messages.error(request, "Problem not found.")
            return redirect("core:problems")

        # verdict = submit_code(problem, code, language)
        verdict = None

        # Save submission
        Submission.objects.create(
            user=user,
            problem=problem,
            code=code,
            verdict=verdict,
            language=language,
            submitted_at=timezone.now(),
        )

        # # Handle verdict
        # if verdict is None:
        #     messages.error(request, "Submission failed. Please try again.")
        #     return redirect("core:problem_detail", pk=problem.id)
        # elif verdict == "AC":
        #     messages.success(request, "Your solution was accepted!")
        # else:
        #     messages.error(request, f"Submission failed with verdict {verdict}")

        messages.success(
            request, f"Your solution was submitted with verdict: {verdict}"
        )
        return redirect("core:problem_detail", pk=problem.id)

    return redirect("core:problems")
