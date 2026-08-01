import os
from config import set_limit

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads files in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to read files from, relative to the working directory (default is the working directory itself)",
                },
            },
        "required": ["file_path",]
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs    
        valid_file = os.path.isfile(target_path)

        if not valid_path:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not valid_file:
                return f'Error: File not found or is not a regular file: "{file_path}"'

        
        with open(target_path, "r") as file:
            file_contents = file.read(set_limit)
            if file.read(1):
                        file_contents += f'[...File "{file_path}" truncated at {set_limit} characters]'
            return file_contents
        

    except Exception as e:
        return f"Error reading file: {e}"

