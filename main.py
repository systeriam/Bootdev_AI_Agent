import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse



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
    args = parser.parse_args()
    # Now we can access `args.user_prompt`    

# The actual response from the client

    response = client.chat.completions.create(model="openrouter/free", messages = [
        {
            "role": "user",
            "content": f"{args.user_prompt}",
        }
    ])
    if response.usage is not None:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        raise RuntimeError("Failed API request!")
    print(response.choices[0].message.content)



if __name__ == "__main__":
    main()
