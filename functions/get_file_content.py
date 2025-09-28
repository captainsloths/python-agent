# get_file_content.py
import os
import config


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)

        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(full_path)

        if os.path.isabs(file_path) and not abs_target_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isabs(file_path):
            # Normalize the path to handle .. and . properly
            normalized_target = os.path.normpath(abs_target_path)
            normalized_working = os.path.normpath(abs_working_dir)

            if not (normalized_target.startswith(normalized_working + os.sep) or normalized_target == normalized_working):
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the path exists and is a regular file
        if not os.path.exists(abs_target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        if not os.path.isfile(abs_target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file content
        with open(abs_target_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Truncate if necessary
        if len(content) > config.MAX_CHARS:
            content = content[:config.MAX_CHARS]
            content += f'[...File "{file_path}" truncated at {
                config.MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"
