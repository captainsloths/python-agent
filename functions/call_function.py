from google.genai import types
from functions.get_into_files import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def call_function(function_call_part, verbose=False):

    # Dictionary mapping function names to actual functions
    available_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    function_name = function_call_part.name
    function_args = dict(function_call_part.args)

    # Print function call info
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # Check if function exists
    if function_name not in available_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Add working_directory to the arguments
    function_args["working_directory"] = "./calculator"

    # Call the function
    try:
        function_to_call = available_functions[function_name]
        function_result = function_to_call(**function_args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )

    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error calling {
                        function_name}: {str(e)}"},
                )
            ],
        )
