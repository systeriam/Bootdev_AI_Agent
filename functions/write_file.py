import os


# JSON Schemas are kinda confusing, yo
# One big nested python dictionary of strings written in javascript syntax
# so that the LLM can interpret, or something of that effect
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes files in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write files from, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write",
                },
            },
        "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        is_directory = os.path.isdir(target_path)

        if not valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if is_directory:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        print(repr(os.path.dirname(target_path)))
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as file:
                    file.write(content)
                    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
                    

    except Exception as e:
        return f'Error writing files: {e}'