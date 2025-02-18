# --------------------------------------------------------------
# Import Modules
# --------------------------------------------------------------

import os
import json
import openai
from dotenv import load_dotenv
import requests


# --------------------------------------------------------------
# Load OpenAI API Token From the .env File
# --------------------------------------------------------------

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

def get_wind_speed(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    print("\n\ndata:", data)
    return data['current']['wind_speed_10m']

def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)
    if name == "get_wind_speed":
        return get_wind_speed(**args)

client = openai.OpenAI()

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
},
{
    "type": "function",
    "function": {
        "name": "get_wind_speed",
        "description": "Get current wind speed for provided coordinates in km/h.",
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

messages = [{"role": "user", "content": "What's the wind speed and temperature like in Paris today?"}]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

print(completion)

print("\n\n\n===============================\n\n\n")

print(completion.choices[0].message.tool_calls)


# tool_call = completion.choices[0].message.tool_calls[0]
# args = json.loads(tool_call.function.arguments)

# result = get_weather(args["latitude"], args["longitude"])

# messages.append(completion.choices[0].message)  # append model's function call message
# messages.append({                               # append result message
#     "role": "tool",
#     "tool_call_id": tool_call.id,
#     "content": str(result)
# })

messages.append(completion.choices[0].message)  # append model's function call message
for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    result = call_function(name, args)
    print("\n\nResult: ", result)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result)
    })

print("\n\nMessages:", messages)

completion_2 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

print("\n\n\n===============================\n\n\n")

print(completion_2.choices[0].message.content)