# --------------------------------------------------------------
# Import Modules
# --------------------------------------------------------------

import os
import json
import openai
from dotenv import load_dotenv
import requests


# --------------------------------------------------------------
# Sample function code stored in your local machine
# --------------------------------------------------------------

def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

# --------------------------------------------------------------
# Load OpenAI API Token From the .env File
# --------------------------------------------------------------

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

# --------------------------------------------------------------
# Define function definition for OpenAI model to use
# --------------------------------------------------------------

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

# --------------------------------------------------------------
# Sample user request
# --------------------------------------------------------------

messages = [{"role": "user", "content": "What's the weather like in Paris today?"}]


# --------------------------------------------------------------
# Let OpenAI model decide what function to call
# --------------------------------------------------------------

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

# print(completion)

# print("\n\n\n===============================\n\n\n")

# print(completion.choices[0].message.tool_calls)


# --------------------------------------------------------------
# Execute the local function code based on OpenAI's prediction
# --------------------------------------------------------------

tool_call = completion.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

result = get_weather(args["latitude"], args["longitude"])


# --------------------------------------------------------------
# Supply OpenAI model with results and print response for users in Natural Language
# --------------------------------------------------------------

messages.append(completion.choices[0].message)  # append model's function call message
messages.append({                               # append result message
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})

# print("\n\nMessages:", messages)

completion_2 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

# print("\n\n\n===============================\n\n\n")

print(completion_2.choices[0].message.content)