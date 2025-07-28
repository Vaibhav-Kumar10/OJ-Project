from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Problem, Submission
from contests.models import ProblemCompletion, UserScore
from google import genai
import markdown
import os

# import google.generativeai as genai


# ----------------- Home Page ----------------- #
def home_view(request):
    featured_problems = []

    if request.user.is_authenticated:
        featured_problems = (
            ProblemCompletion.objects.filter(user=request.user, is_complete=True)
            .select_related("problem")
            .order_by("-score_awarded")[:4]
        )

    scores = UserScore.objects.select_related("user").order_by(
        "-score", "-problems_solved"
    )

    context = {
        "featured_problems": featured_problems,
        "scores": scores,
    }

    return render(request, "core/home.html", context)


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


@login_required
def dashboard_view(request):
    return render(request, "core/dashboard.html")


@login_required
def get_ai_review(request):
    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("language")
        problem_id = request.POST.get("problem_id")
        input_data = request.POST.get("input_data", "")
        problem = get_object_or_404(Problem, id=problem_id)

        try:
            # The client gets the API key from the environment variable `GEMINI_API_KEY`.
            client = genai.Client()

            prompt = (
                "You're an expert code reviewer.\n"
                "Given the following code and problem statement, provide a short, clear review focusing on performance, style, and correctness.\n"
                f"Problem:\n{problem.statement}\n"
                f"Code ({language}):\n{code}"
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            ai_review = response.text

        except Exception as e:
            ai_review = f"⚠️ AI Review failed: {str(e)}"

        ai_review = markdown.markdown(ai_review)

        # Pull previous submissions
        submissions = Submission.objects.filter(
            user=request.user, problem=problem
        ).order_by("-submitted_at")

        return render(
            request,
            "core/problem_detail.html",
            {
                "problem": problem,
                "submissions": submissions,
                "code": code,
                "language": language,
                "input_data": input_data,
                "ai_review": ai_review,
            },
        )

    return redirect("core:problems")
