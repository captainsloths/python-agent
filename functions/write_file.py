# write_file.py
import os


def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)

        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(full_path)

        if os.path.isabs(file_path) and not abs_target_path.abs_target_path(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.isabs(file_path):
            normalized_target = os.path.normpath(abs_target_path)
            normalized_working = os.path.normpath(abs_working_dir)

            if not (normalized_target.startswith(normalized_working + os.sep) or normalized_target == normalized_working):
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Create director if it doesn't exist
        target_dir = os.path.dirname(abs_target_path)
        if target_dir and not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with open(abs_target_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"
