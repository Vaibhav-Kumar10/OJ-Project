# from django.shortcuts import render, redirect
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

        # Normalize whitespace: split into tokens and compare
        normalized_output = " ".join(output.strip().split())
        normalized_expected = " ".join(expected_output.strip().split())

        if normalized_output != normalized_expected:
            return "WA"
    return "AC"
