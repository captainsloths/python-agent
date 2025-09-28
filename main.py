import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT
from functions.get_into_files import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    print("Hello from python-agent!")
    if len(sys.argv) < 2:
        print("Usage: script.py 'your prompt here'")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    # Initialize conversation with user's prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_run_python_file,
            schema_write_file,
            schema_get_file_content,
        ]
    )

    # Main agent loop - up to 20 iterations
    for iteration in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=SYSTEM_PROMPT
                ),
            )

            # Add the model's response to the conversation
            if response.candidates and response.candidates[0].content:
                messages.append(response.candidates[0].content)

            # Check if the response has function calls
            has_function_calls = False
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        has_function_calls = True

                        # Call the requested function
                        function_call_result = call_function(
                            part.function_call, verbose)

                        # Verify response structure
                        if not hasattr(function_call_result, 'parts') or not function_call_result.parts:
                            raise Exception(
                                "Function call result missing expected parts")
                        if not hasattr(function_call_result.parts[0], 'function_response'):
                            raise Exception(
                                "Function call result missing function_response")

                        # Print function result if verbose
                        if verbose:
                            print(
                                f"-> {function_call_result.parts[0].function_response.response}")

                        # Add function result to conversation as a user message
                        messages.append(function_call_result)

            # If there's text response and no function calls, we're done
            if response.text and not has_function_calls:
                print("Final response:")
                print(response.text)
                break

            # If we have text but also function calls, continue the loop
            # (the function results were added to messages above)

        except Exception as e:
            print(f"Error in iteration {iteration + 1}: {e}")
            break

    # Print token usage if verbose
    if verbose and 'response' in locals():
        response_tokens = response.usage_metadata.candidates_token_count
        prompt_tokens = response.usage_metadata.prompt_token_count
        print(f"User prompt: {user_prompt}")
        print(f"Final prompt tokens: {prompt_tokens}")
        print(f"Final response tokens: {response_tokens}")
        print(f"Total iterations: {iteration + 1}")


if __name__ == "__main__":
    main()
