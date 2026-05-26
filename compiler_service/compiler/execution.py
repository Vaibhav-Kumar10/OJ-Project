"""
Windows

import subprocess
import tempfile
import os
import re
import signal


def execute_code(language, code, input_data):
    try:
        if language == "python":
            suffix = ".py"
            if os.name == "nt":  # Windows
                command = ["python"]
                # or command = ["py"]
            else:  # Linux/macOS
                command = ["python3"]

        elif language == "cpp":
            suffix = ".cpp"
        elif language == "java":
            suffix = ".java"
        else:
            return "Error: Unsupported language"

        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = os.path.join(temp_dir, f"Main{suffix}")
            with open(source_path, "w") as source_file:
                if language == "java":
                    # Ensure public class is named Main
                    code = re.sub(
                        r"(public\s+)?class\s+\w+",
                        "public class Main",
                        code,
                        count=1,
                    )
                source_file.write(code)

            if language == "cpp":
                executable_path = os.path.join(temp_dir, "a.out")
                compile_proc = subprocess.run(
                    ["g++", source_path, "-o", executable_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                if compile_proc.returncode != 0:
                    return compile_proc.stderr.decode().strip()
                command = [executable_path]

            elif language == "java":
                compile_proc = subprocess.run(
                    ["javac", source_path],
                    cwd=temp_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                if compile_proc.returncode != 0:
                    return compile_proc.stderr.decode().strip()
                command = ["java", "-cp", temp_dir, "Main"]
            elif language == "python":
                command.append(source_path)

            exec_proc = subprocess.run(
                command,
                input=input_data.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5,
                creationflags=(
                    subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
                ),
                preexec_fn=os.setsid if os.name != "nt" else None,
            )
            # exec_proc = subprocess.run(
            #     command,
            #     input=input_data.encode(),
            #     stdout=subprocess.PIPE,
            #     stderr=subprocess.PIPE,
            #     timeout=5,
            #     preexec_fn=os.setsid,  # run in its own process group
            # )

            return (exec_proc.stdout.decode() or exec_proc.stderr.decode()).strip()

        # except subprocess.TimeoutExpired:
        #     os.killpg(os.getpgid(exec_proc.pid), signal.SIGTERM)
        #     return "Error: Code execution timed out"
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out"

    except Exception as e:
        return f"Error: {str(e)}"


"""

# Docker
import subprocess
import tempfile
import os
import re
import signal
import sys

# Limits
EXECUTION_TIMEOUT = 5
COMPILATION_TIMEOUT = 10
MAX_OUTPUT_SIZE = 1024 * 1024  # 1 MB


def execute_code(language, code, input_data=""):
    try:
        if language == "python":
            suffix = ".py"

        elif language == "cpp":
            suffix = ".cpp"

        elif language == "java":
            suffix = ".java"

        else:
            return "Error: Unsupported language"

        with tempfile.TemporaryDirectory() as temp_dir:

            source_path = os.path.join(temp_dir, f"Main{suffix}")

            with open(source_path, "w", encoding="utf-8") as source_file:

                if language == "java":

                    code = re.sub(r"^\s*package\s+.*?;", "", code, flags=re.MULTILINE)

                    code = re.sub(
                        r"(public\s+)?class\s+\w+", "public class Main", code, count=1
                    )

                source_file.write(code)

            # Build compile/run command

            if language == "python":

                command = [sys.executable, source_path]

            elif language == "cpp":

                executable = os.path.join(temp_dir, "Main")

                compile_proc = subprocess.run(
                    [
                        "g++",
                        source_path,
                        "-O2",
                        "-std=c++17",
                        "-o",
                        executable,
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=COMPILATION_TIMEOUT,
                )

                if compile_proc.returncode != 0:
                    return compile_proc.stderr.decode(errors="replace").strip()

                command = [executable]

            elif language == "java":

                compile_proc = subprocess.run(
                    ["javac", source_path],
                    cwd=temp_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=COMPILATION_TIMEOUT,
                )

                if compile_proc.returncode != 0:
                    return compile_proc.stderr.decode(errors="replace").strip()

                command = ["java", "-Xmx128m", "-cp", temp_dir, "Main"]

            # Create isolated process group

            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=temp_dir,
                shell=False,
                preexec_fn=os.setsid,
            )

            try:

                stdout, stderr = process.communicate(
                    input=input_data.encode(),
                    timeout=EXECUTION_TIMEOUT,
                )

            except subprocess.TimeoutExpired:

                try:
                    os.killpg(
                        os.getpgid(process.pid),
                        signal.SIGKILL,
                    )
                except Exception:
                    pass

                return "Error: Time Limit Exceeded"

            output = stdout + stderr

            if len(output) > MAX_OUTPUT_SIZE:

                try:
                    os.killpg(
                        os.getpgid(process.pid),
                        signal.SIGKILL,
                    )
                except Exception:
                    pass

                return "Error: Output Limit Exceeded"

            process.wait()
            return output.decode(errors="replace").strip()

    except subprocess.TimeoutExpired:
        return "Error: Compilation Timeout"

    except Exception as e:
        return f"Error: {e}"


# """
