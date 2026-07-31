import subprocess
import os

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs    
        valid_file = os.path.isfile(target_path)
        

        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not valid_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]

        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command, 
            cwd=working_directory, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            timeout=30)

        result_out = ""

        if result.returncode != 0:
            result_out += f"Process exited with code {result.returncode}\n"
        if len(result.stdout) == 0  and len(result.stderr) == 0:
            result_out += "No output produced\n"
        else:
            result_out += f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        return result_out
    except Exception as e:
        return f"Error: executing Python file: {e}"