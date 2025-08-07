from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .execution import execute_code
from .evaluation import submit_code
from contests.models import UserScore, ProblemCompletion
from core.models import Problem, Submission
from core.utils import is_similar

@login_required
def run_code_view(request):
    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("language")
        input_data = request.POST.get("input_data", "")
        problem_id = request.POST.get("problem_id")

        try:
            output = execute_code(language, code, input_data)
        except Exception as e:
            output = f"Error: {str(e)}"

        problem = Problem.objects.get(id=problem_id)
        submissions = Submission.objects.filter(
            user=request.user, problem=problem
        ).order_by("-submitted_at")

        context = {
            "problem": problem,
            "submissions": submissions,
            "output": output,
            "code": code,
            "input_data": input_data,
            "language": language,
            "mode": "run",
        }

        return render(request, "core/problem_detail.html", context=context)
    return redirect("core:problems")


@login_required
def submit_code_view(request):
    if request.method == "POST":
        user = request.user
        problem_id = request.POST.get("problem_id")
        code = request.POST.get("code")
        language = request.POST.get("language")
        problem = Problem.objects.get(id=problem_id)

        # Check for similarity with previous submissions (by other users)
        past_submissions = Submission.objects.filter(problem=problem).exclude(user=user)

        for sub in past_submissions:
            if is_similar(code, sub.code):
                messages.warning(
                    request, "⚠️ Your code is too similar to another user's submission."
                )
                verdict = "Possible Plagiarism"
                break
        else:
            output = submit_code(problem, code, language)

            if output == "AC":
                verdict = "Accepted"

                problem_status, _ = ProblemCompletion.objects.get_or_create(
                    user=user, problem=problem
                )

                if not problem_status.is_complete:
                    problem_status.is_complete = True
                    problem_status.score_awarded = problem.score
                    problem_status.save()

                    user_score, _ = UserScore.objects.get_or_create(user=user)
                    user_score.score += problem.score
                    user_score.problems_solved += 1
                    user_score.save()

                messages.success(request, "Your solution was accepted!")

            elif output == "WA":
                verdict = "Wrong Answer"
                messages.error(request, f"Submission failed with verdict {verdict}")

            else:
                verdict = "Submission Failed"
                messages.error(request, f"Submission failed with verdict {output}")

        # Save submission
        Submission.objects.create(
            user=user,
            problem=problem,
            code=code,
            verdict=verdict,
            language=language,
            submitted_at=timezone.now(),
        )

        user_submissions = Submission.objects.filter(
            user=user, problem=problem
        ).order_by("-submitted_at")

        context = {
            "problem": problem,
            "submissions": user_submissions,
            "code": code,
            "language": language,
            "mode": "submit",
        }

        return render(request, "core/problem_detail.html", context=context)
    return redirect("core:problems")
