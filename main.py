import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import *

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
        tools=available_functions,
        temperature=0
        )

    message = response.choices[0].message

    


# Call available functions, if applicable
    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if not result_message["content"]:
                raise Exception("Tool message is empty")
            if args.verbose:
                print(f"-> {result_message['content']}")
            

 # If verbose is set, print extra data
# Otherwise just print response
    
    if response.choices[0].message.content is not None:
            print(response.choices[0].message.content)
    

    if args.verbose == True:
        if response.usage is not None:
            print("VERBOSE:")
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            raise RuntimeError("Failed API request!")
    
                    
            
                




if __name__ == "__main__":
    main()
