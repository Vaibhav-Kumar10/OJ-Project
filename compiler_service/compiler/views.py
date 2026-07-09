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
            output, success = execute_code(language, code, input_data)
            return JsonResponse({"output": output, "success": success})
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Execution error: {e}", exc_info=True)
            return JsonResponse({"error": "An internal error occurred during execution.", "success": False}, status=500)
    return JsonResponse({"error": "Invalid request method", "success": False}, status=400)
