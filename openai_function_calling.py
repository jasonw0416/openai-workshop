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
#  -    there are two functions, get_weather and get_wind_speed, and 
#       call_functions that determine which function to call based on
#       OpenAI's response
# --------------------------------------------------------------

def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

def get_wind_speed(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['wind_speed_10m']

# We need this function because of how OpenAI returns "function calls." If you remember from the last part,
# the response contains a list of "tool call" objects that each have a name and arguments. We were able to
# ignore this last time since we only had one function. But now since we have multiple functions, we have to 
# figure out what function OpenAI wants to call based on the tool call object's name.
def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)
    if name == "get_wind_speed":
        return get_wind_speed(**args)

# --------------------------------------------------------------
# Load OpenAI API Token From the .env File
# --------------------------------------------------------------

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()


# --------------------------------------------------------------
# Define function definition for OpenAI model to use. Notice there are two functions now
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

# --------------------------------------------------------------
# Sample user request
# --------------------------------------------------------------

while True:
    city = input("Enter the city you'd like to learn more about for today (or type 'exit' to quit): ").strip()
    if city.lower() == "exit":
        break

    what_they_want = input("What would you like to know about the city? (temperature/wind speed/both): ").strip().lower()
    if what_they_want == "both" or what_they_want not in ["temperature", "wind speed", "both"]:
        what_they_want = "temperature and wind speed"

    messages = [{"role": "user", "content": f"What's the {what_they_want} like in {city} today?"}]

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

    print("\n\n===============================\n\n")

    print(f"Based off user input, the function(s) you should call are:")
    for tool_call in completion.choices[0].message.tool_calls:
        name = tool_call.function.name
        print(f"{name}()")

    print("\n\n===============================\n\n")


    # --------------------------------------------------------------
    # Execute the local function code based on OpenAI's prediction
    # --------------------------------------------------------------

    # Just like before, we will use the result of our function call to make another request to OpenAI.
    # We again append the result of our first request to the list—this is what OpenAI sent us back in response to our first question.
    messages.append(completion.choices[0].message)

    # Since we can expect multiple tool calls now, we now loop through the list of tool calls and call each function.
    for tool_call in completion.choices[0].message.tool_calls:
        # Here, we take the relevant information from the tool call object
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        # And then use it to call the function
        result = call_function(name, args)

        # Finally, we add a message with the result for that function call.
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

    # print("\n\nMessages:", messages)

    # --------------------------------------------------------------
    # Supply OpenAI model with results and print response for users in Natural Language
    # --------------------------------------------------------------

    # To end, we make another request to OpenAI with the updated messages list.
    # This is the same thing we did before, except we are now able to supply OpenAI with the 
    # results of multiple function calls, not just a single one.
    completion_2 = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )

    # print("\n\n\n===============================\n\n\n")

    print(completion_2.choices[0].message.content)