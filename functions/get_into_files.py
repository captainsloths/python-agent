import os


def get_files_info(working_directory, directory="."):
    try:
        # Create the full path by joining working_directory and directory
        full_path = os.path.join(working_directory, directory)

        # Get absolute paths for security validation
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(full_path)

        # For absolute paths like "/bin", they won't start with our working directory
        if os.path.isabs(directory) and not abs_target_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # For relative paths, use a more thorough check
        if not os.path.isabs(directory):
            # Normalize the path to handle .. and . properly
            normalized_target = os.path.normpath(abs_target_path)
            normalized_working = os.path.normpath(abs_working_dir)

            # Check if the normalized target is outside the working directory
            if not (normalized_target.startswith(normalized_working + os.sep) or normalized_target == normalized_working):
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the path exists and is a directory
        if not os.path.exists(abs_target_path):
            return f'Error: "{directory}" does not exist'

        if not os.path.isdir(abs_target_path):
            return f'Error: "{directory}" is not a directory'

        # List directory contents
        files_info = []
        for item in os.listdir(abs_target_path):
            item_path = os.path.join(abs_target_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            files_info.append(
                f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(files_info)

    except Exception as e:
        return f"Error: {str(e)}"
