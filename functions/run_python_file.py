# run_python_file.py
import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command line arguments to pass to the Python file",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)

        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(full_path)

        if os.path.isabs(file_path) and not abs_target_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isabs(file_path):
            normalized_target = os.path.normpath(abs_target_path)
            normalized_working = os.path.normpath(abs_working_dir)

            if not (normalized_target.startswith(normalized_working + os.sep) or normalized_target == normalized_working):
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_target_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        cmd = ['python', abs_target_path] + args

        completed_process = subprocess.run(
            cmd,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_lines = []

        if completed_process.stdout:
            output_lines.append(f"STDOUT:\n{completed_process.stdout}")

        # Add stderr if present
        if completed_process.stderr:
            output_lines.append(f"STDERR:\n{completed_process.stderr}")

        # Add exit code if non-zero
        if completed_process.returncode != 0:
            output_lines.append(f"Process exited with code {
                                completed_process.returncode}")

        # Return the formatted output or "No output produced."
        if output_lines:
            return "\n".join(output_lines)
        else:
            return "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"
