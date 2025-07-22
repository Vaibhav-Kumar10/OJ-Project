from django.shortcuts import render, redirect
from .execution import execute_code


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

        from core.models import Problem, Submission

        problem = Problem.objects.get(id=problem_id)
        submissions = Submission.objects.filter(
            user=request.user, problem=problem
        ).order_by("-submitted_at")

        return render(
            request,
            "core/problem_detail.html",
            {
                "problem": problem,
                "submissions": submissions,
                "output": output,
                "code": code,
                "input_data": input_data,
                "language": language,
            },
        )

    return redirect("core:problems")


def submit_code_view(request):
    # problem_id = request.POST.get("problem_id")
    # testcases = TestCase.objects.get(pk_id=problem_id)
    # for testcase in testcases:
    #     run_code()
    pass
