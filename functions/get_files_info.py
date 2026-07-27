import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        valid = os.path.isdir(target_dir)

        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if valid == False:
            return f'Error: "{directory}" is not a directory'

        if valid_target_dir == True:
            contents = os.listdir(target_dir)
            content_list = []
            #print(f'Success: "{directory}" is within the working directory')
            for item in contents:
                file_path = os.path.join(target_dir, item)
                try:
                    content_list.append(f"- {item}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
                except Exception:
                    return "Error: File unsupported"
            return "\n".join(content_list)
    except Exception as e:
        return f"Error listing files: {e}"
