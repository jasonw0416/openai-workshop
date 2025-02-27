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
    # FIGURE OUT WHICH FUNCTION TO CALL BASED ON NAME HERE!
    pass

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
        # ADD FUNCTION DETAILS HERE!
        "strict": True
    }
}]

# --------------------------------------------------------------
# Sample user request
# --------------------------------------------------------------

while True:
    # GET USER INPUT HERE!
    # this time, get input in two stages:
    # 1. Get the city name
    # 2. Get the type of weather they want to know about (temperature, wind speed, or both?)

    messages = [{"role": "user", "content": f"What's the weather like in Los Angeles today?"}]

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
        # ADD RESULT MESSAGE HERE!

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