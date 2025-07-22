from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Problem, Submission, TestCase
from compiler.execution import execute_code as run_c


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


# ----------------- Run Code ----------------- #
# @login_required
# def run_code(request):
#     if request.method == "POST":
#         user = request.user
#         problem_id = request.POST.get("problem_id")
#         language = request.POST.get("language")
#         code = request.POST.get("code")

#         try:
#             problem = Problem.objects.get(id=problem_id)
#         except Problem.DoesNotExist:
#             messages.error(request, "Problem not found.")
#             return redirect("core:problems")

#         try:
#             output = run_c(language, code)
#         except Exception as e:
#             output = f"Error: {str(e)}"

#         # Save submission
#         Submission.objects.create(
#             user=user,
#             problem=problem,
#             code=code,
#             verdict=output,
#             language=language,
#             submitted_at=timezone.now(),
#         )

#         user_submissions = Submission.objects.filter(
#             user=user, problem=problem
#         ).order_by("-submitted_at")

#         return render(
#             request,
#             "core/problem_detail.html",
#             {
#                 "problem": problem,
#                 "submissions": user_submissions,
#                 "output": output,
#             },
#         )
#     return redirect("core:problems")
