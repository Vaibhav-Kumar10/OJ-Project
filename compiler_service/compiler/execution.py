import subprocess
import tempfile
import os
import re
import signal


def execute_code(language, code, input_data):
    try:
        if language == "python":
            suffix = ".py"
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
                    code = re.sub(r"public\s+class\s+\w+", "public class Main", code)
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
                preexec_fn=os.setsid,  # run in its own process group
            )
            return (exec_proc.stdout.decode() or exec_proc.stderr.decode()).strip()
        
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(exec_proc.pid), signal.SIGTERM)
        return "Error: Code execution timed out"
    except Exception as e:
        return f"Error: {str(e)}"
