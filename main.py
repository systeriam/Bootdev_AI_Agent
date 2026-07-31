import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt


def main():
# Load environmental variables from .env
    

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API KEY NOT FOUND!")

# Import OpenAI class and create client
    

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

# User input

    parser = argparse.ArgumentParser(description="AI Assistant")
    parser.add_argument("user_prompt", type=str, help="Input prompt:")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`    

# The actual response from the client

    response = client.chat.completions.create(
        model="openrouter/free", 
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt}
        ],
        temperature=0
        )
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(response.choices[0].message.content)
        if response.usage is not None:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            raise RuntimeError("Failed API request!")
    else:
        print(response.choices[0].message.content)




if __name__ == "__main__":
    main()
