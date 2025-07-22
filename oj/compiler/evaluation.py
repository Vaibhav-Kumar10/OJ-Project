from django.shortcuts import render, redirect
from core.models import TestCase
from .execution import execute_code


def submit_code(problem, code, language):
    testcases = TestCase.objects.filter(problem=problem)

    for testcase in testcases:
        input_data = testcase.input_data.strip()
        expected_output = testcase.output.strip()

        try:
            output = execute_code(language, code, input_data).strip()
        except Exception as e:
            return f"Error: {e}"

        if output.strip() != expected_output.strip():
            return "WA"
        return "AC"
