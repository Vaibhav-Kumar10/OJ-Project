from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .execution import execute_code


@csrf_exempt
def run_code_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            language = data.get("language")
            code = data.get("code")
            input_data = data.get("input_data", "")
            output = execute_code(language, code, input_data)
            return JsonResponse({"output": output})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)
