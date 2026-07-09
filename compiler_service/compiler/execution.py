# Docker
import subprocess
import tempfile
import os
import re
import signal
import sys

# Linux resource limits (Docker/Linux only)
try:
    import resource
except ImportError:
    resource = None


# ----------------------------
# Limits
# ----------------------------
EXECUTION_TIMEOUT = 5
COMPILATION_TIMEOUT = 10

MAX_OUTPUT_SIZE = 1024 * 1024  # 1 MB
MAX_INPUT_SIZE = 1024 * 1024  # 1 MB

MEMORY_LIMIT_MB = 256


def limit_resources():
    """
    Linux-only resource limits.
    Runs inside child process before execution.
    """

    if resource is None:
        return

    memory_bytes = MEMORY_LIMIT_MB * 1024 * 1024

    try:

        # Virtual memory cap
        resource.setrlimit(
            resource.RLIMIT_AS,
            (memory_bytes, memory_bytes),
        )

        # CPU seconds cap
        resource.setrlimit(
            resource.RLIMIT_CPU,
            (
                EXECUTION_TIMEOUT + 1,
                EXECUTION_TIMEOUT + 1,
            ),
        )

        # Limit open files
        resource.setrlimit(
            resource.RLIMIT_NOFILE,
            (32, 32),
        )

        # Disable fork bombs
        if hasattr(resource, "RLIMIT_NPROC"):
            resource.setrlimit(
                resource.RLIMIT_NPROC,
                (32, 32),
            )

    except Exception:
        pass


def get_preexec():
    """
    Linux Docker:
        create process group + limits (for user code execution)

    Windows:
        return None
    """

    if os.name == "nt":
        return None

    def setup():
        os.setsid()
        limit_resources()

    return setup


def get_compile_preexec():
    """
    Preexec for compilation steps (g++, javac) — no RLIMIT_AS, no RLIMIT_NPROC.

    - g++  spawns cc1plus, as, ld as child processes → needs NPROC headroom
    - javac runs inside a JVM → needs GB of virtual address space (like java)

    Docker's mem_limit: 1g already enforces actual RAM limits on the container,
    so RLIMIT_AS is unnecessary and actively harmful for both compilers.
    Only a CPU time cap is applied to prevent runaway compilations.
    """

    if os.name == "nt":
        return None

    def setup():
        os.setsid()
        if resource is None:
            return
        try:
            resource.setrlimit(
                resource.RLIMIT_CPU,
                (COMPILATION_TIMEOUT + 1, COMPILATION_TIMEOUT + 1),
            )
        except Exception:
            pass

    return setup


def get_java_preexec():
    """
    Preexec for Java EXECUTION only — no RLIMIT_AS, no RLIMIT_NPROC, no RLIMIT_NOFILE.

    The JVM needs:
    - Gigabytes of virtual address space (RLIMIT_AS would crash it)
    - 20+ internal threads: GC, Signal Dispatcher, VM Thread, Finalizer,
      Compiler threads, etc. (RLIMIT_NPROC=32 causes pthread_create EAGAIN)
    - Many file descriptors for class loading (RLIMIT_NOFILE=32 is too low)

    Memory is controlled by JVM flags: -Xmx, -XX:MaxMetaspaceSize, etc.
    Docker's mem_limit: 1g provides the final hard ceiling.
    Only a CPU time cap is applied to prevent infinite loops.
    """

    if os.name == "nt":
        return None

    def setup():
        os.setsid()
        if resource is None:
            return
        try:
            resource.setrlimit(
                resource.RLIMIT_CPU,
                (EXECUTION_TIMEOUT + 1, EXECUTION_TIMEOUT + 1),
            )
        except Exception:
            pass

    return setup


def cleanup_process(process):
    """
    Kill process safely.
    """

    try:

        if os.name == "nt":

            process.kill()

        else:

            os.killpg(
                os.getpgid(process.pid),
                signal.SIGKILL,
            )

    except Exception:
        pass


def normalize_java(code):

    # Remove package declaration
    code = re.sub(
        r"^\s*package\s+[^;]*;",
        "",
        code,
        flags=re.MULTILINE,
    )

    # Rename public class -> Main
    match = re.search(
        r"public\s+class\s+(\w+)",
        code,
    )

    if match:

        original = match.group(1)

        code = code.replace(
            f"public class {original}",
            "public class Main",
            1,
        )

    return code


def execute_code(language, code, input_data=""):

    try:

        if len(input_data.encode("utf-8")) > MAX_INPUT_SIZE:
            return "Error: Input Too Large", False

        suffix_map = {
            "python": ".py",
            "cpp": ".cpp",
            "java": ".java",
        }

        if language not in suffix_map:
            return "Error: Unsupported language", False

        suffix = suffix_map[language]

        with tempfile.TemporaryDirectory() as temp_dir:

            source_path = os.path.join(
                temp_dir,
                f"Main{suffix}",
            )

            if language == "java":
                code = normalize_java(code)

            with open(
                source_path,
                "w",
                encoding="utf-8",
            ) as f:

                f.write(code)

            # ------------------------
            # Compile
            # ------------------------

            if language == "cpp":

                executable = os.path.join(
                    temp_dir,
                    "Main",
                )

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
                    preexec_fn=get_compile_preexec(),
                )

                if compile_proc.returncode != 0:

                    compile_output = compile_proc.stdout + compile_proc.stderr

                    return compile_output.decode(errors="replace").strip(), False

                command = [executable]

            elif language == "java":

                compile_proc = subprocess.run(
                    [
                        "javac",
                        source_path,
                    ],
                    cwd=temp_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=COMPILATION_TIMEOUT,
                    preexec_fn=get_compile_preexec(),
                )

                if compile_proc.returncode != 0:

                    compile_output = compile_proc.stdout + compile_proc.stderr

                    return compile_output.decode(errors="replace").strip(), False

                command = [
                    "java",
                    "-Xmx128m",                      # max heap 128 MB
                    "-Xms16m",                       # initial heap 16 MB
                    "-Xss512k",                      # thread stack 512 KB
                    "-XX:+UseSerialGC",              # minimal GC overhead
                    "-XX:ReservedCodeCacheSize=32m", # cap JIT code cache (default=240MB!)
                    "-XX:MaxMetaspaceSize=64m",      # cap class metadata
                    "-XX:TieredStopAtLevel=1",       # disable full JIT (saves memory)
                    "-cp",
                    temp_dir,
                    "Main",
                ]

            else:

                command = [
                    sys.executable,
                    source_path,
                ]

            # ------------------------
            # Run
            # ------------------------

            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=temp_dir,
                shell=False,
                preexec_fn=get_java_preexec() if language == "java" else get_preexec(),
            )

            try:

                stdout, stderr = process.communicate(
                    input=input_data.encode(),
                    timeout=EXECUTION_TIMEOUT,
                )

            except subprocess.TimeoutExpired:

                cleanup_process(process)

                return "Error: Time Limit Exceeded", False

            output = stdout + stderr

            if len(output) > MAX_OUTPUT_SIZE:

                cleanup_process(process)

                return "Error: Output Limit Exceeded", False

            return output.decode(errors="replace").strip(), (process.returncode == 0)

    except subprocess.TimeoutExpired:

        return "Error: Compilation Timeout", False

    except MemoryError:

        return "Error: Memory Limit Exceeded", False

    except Exception as e:

        return f"Error: {str(e)}", False


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
