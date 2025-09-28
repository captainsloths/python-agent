import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT
from functions.get_into_files import schema_get_files_info

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

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT),
    )

    response_tokens = response.usage_metadata.candidates_token_count
    prompt_tokens = response.usage_metadata.prompt_token_count

    # print(response.text)
    has_function_calls = False
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call') and part.function_call:
                has_function_calls = True
                print(f"Calling function: {part.function_call.name}({
                      dict(part.function_call.args)})")

    if response.text and not has_function_calls:
        print(response.text)

    if verbose:
        print(f"Gemini: {response.text}")
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
