import requests
import os

COMPILER_URL = "http://13.233.196.157:8000/api/run/"


def execute_code(language, code, input_data):
    try:
        response = requests.post(
            COMPILER_URL,  # Use service name in Docker or actual URL
            json={"language": language, "code": code, "input_data": input_data},
            timeout=10,
        )
        if response.status_code == 200:
            return response.json().get("output", "")
        return f"Error: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


# from django.conf import settings
# import uuid
# import subprocess
# from pathlib import Path


# def execute_code(language, code, input_data):
#     COMPILER_PATH = Path(settings.BASE_DIR) / "compiler"
#     directories = ["codes", "inputs", "outputs"]
#     for directory in directories:
#         dir_path = COMPILER_PATH / directory
#         dir_path.mkdir(parents=True, exist_ok=True)

#     codes_dir = COMPILER_PATH / "codes"
#     inputs_dir = COMPILER_PATH / "inputs"
#     outputs_dir = COMPILER_PATH / "outputs"

#     unique = str(uuid.uuid4())
#     unique_input_file_name = f"{unique}.txt"
#     unique_output_file_name = f"{unique}.txt"

#     input_file_path = inputs_dir / unique_input_file_name
#     output_file_path = outputs_dir / unique_output_file_name

#     with open(input_file_path, "w") as inpf:
#         inpf.write(input_data)

#     # PYTHON
#     if language == "py":
#         unique_codes_file_name = f"{unique}.{language}"
#         codes_file_path = codes_dir / unique_codes_file_name
#         with open(codes_file_path, "w") as cf:
#             cf.write(code)
#         run_py(codes_file_path, input_file_path, output_file_path)

#     elif language == "cpp":
#         unique_codes_file_name = f"{unique}.{language}"
#         codes_file_path = codes_dir / unique_codes_file_name
#         with open(codes_file_path, "w") as cf:
#             cf.write(code)
#         run_cpp(codes_dir, unique, codes_file_path, input_file_path, output_file_path)

#     # JAVA
#     elif language == "java":
#         # Always save as Main.java
#         code = force_class_name_main(code)
#         unique_code_file_name = "Main.java"
#         codes_file_path = codes_dir / unique_code_file_name
#         with open(codes_file_path, "w") as cf:
#             cf.write(code)
#         run_java(codes_dir, "Main", codes_file_path, input_file_path, output_file_path)

#     else:
#         with open(output_file_path, "w") as f:
#             f.write("Unsupported language.")

#     with open(output_file_path, "r") as output_file:
#         output_data = output_file.read()

#     return output_data


# def run_py(codes_file_path, input_file_path, output_file_path):
#     with open(input_file_path, "r") as input_file:
#         with open(output_file_path, "w") as output_file:
#             subprocess.run(
#                 ["python", str(codes_file_path)],
#                 stdin=input_file,
#                 stdout=output_file,
#                 stderr=output_file,
#             )


# def run_cpp(codes_dir, unique, codes_file_path, input_file_path, output_file_path):
#     executable_path = codes_dir / unique
#     compile_result = subprocess.run(
#         ["g++", str(codes_file_path), "-o", str(executable_path)],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )
#     if compile_result.returncode == 0:
#         with open(input_file_path, "r") as input_file:
#             with open(output_file_path, "w") as output_file:
#                 subprocess.run(
#                     [str(executable_path)],
#                     stdin=input_file,
#                     stdout=output_file,
#                     stderr=output_file,
#                 )

#     else:
#         with open(output_file_path, "w") as output_file:
#             output_file.write(compile_result.stderr.decode())


# import re


# def force_class_name_main(code):
#     # Replace any public class with 'Main'
#     code = re.sub(r"public\s+class\s+\w+", "public class Main", code)
#     return code


# def run_java(codes_dir, unique, codes_file_path, input_file_path, output_file_path):
#     class_name = codes_file_path.stem
#     compile_result = subprocess.run(
#         ["javac", str(codes_file_path)],
#         cwd=codes_dir,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )

#     if compile_result.returncode == 0:
#         with (
#             open(input_file_path, "r") as input_file,
#             open(output_file_path, "w") as output_file,
#         ):
#             subprocess.run(
#                 ["java", "-cp", str(codes_dir), class_name],
#                 stdin=input_file,
#                 stdout=output_file,
#                 stderr=output_file,
#             )
#     else:
#         with open(output_file_path, "w") as output_file:
#             output_file.write(compile_result.stderr.decode())
