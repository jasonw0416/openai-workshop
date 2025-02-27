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
        # ENTER FUNCTION DETAILS HERE!
        "strict": True
    }
}]

# --------------------------------------------------------------
# Get user request
# --------------------------------------------------------------

while True:
    # GET USER INPUT HERE!

    # replace BLANK with the city name you receive as input
    messages = [{"role": "user", "content": f"What's the weather like in Los Angeles today?"}]

    # --------------------------------------------------------------
    # Let OpenAI model decide what function to call
    # --------------------------------------------------------------

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )

    print("\n\n===============================\n\n")

    print(f"Based off user input, the function you should call is {completion.choices[0].message.tool_calls[0].function.name}()")

    print("\n\n===============================\n\n")

    # --------------------------------------------------------------
    # Execute the local function code based on OpenAI's prediction
    # --------------------------------------------------------------

    # Since we created our input in such a way that we know we will get a tool_call in 
    # our response, we can access it in our response's message object.
    tool_call = completion.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)

    # At this point, args will be a dictionary with values corresponding to the parameters in the function we sent to OpenAI
    # CALL THE FUNCTION USING THE ARGS FROM OPENAI!

    # --------------------------------------------------------------
    # Supply OpenAI model with results and print response for users in Natural Language
    # --------------------------------------------------------------

    # Now, we use the result of our function call to make another request to OpenAI.
    # First, we append the result of our first request to the list—this is what OpenAI sent us back in response to our first question.
    messages.append(completion.choices[0].message)
    # Then, we append a message with the result for that function call.
    messages.append({                               
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": "REPLACE WITH FUNCTION RESULT"
    })

    # Finally, we make another request to OpenAI with the updated messages list.
    # Here, we're basically asking OpenAI to answer our original question, but now it has the result of our function call to work with.
    completion_2 = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )

    print(completion_2.choices[0].message.content)