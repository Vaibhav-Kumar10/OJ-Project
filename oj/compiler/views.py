from django.shortcuts import render
from .execution import execute_code
from django.http import JsonResponse


def run_code_view(request):
    if request.method == "POST":
        language = request.POST.get("language")
        code = request.POST.get("code")
        input_data = request.POST.get("input_data", "")
        try:
            output = execute_code(language, code, input_data)
            return JsonResponse({"output": output})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)


def submit_code_view(request):
    # problem_id = request.POST.get("problem_id")
    # testcases = TestCase.objects.get(pk_id=problem_id)
    # for testcase in testcases:
    #     run_code()
    pass
