import os
import openai
from dotenv import load_dotenv

# --------------------------------------------------------------
# Load OpenAI API Token From the .env File
# --------------------------------------------------------------

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()


# --------------------------------------------------------------
# Ask ChatGPT Questions!
# --------------------------------------------------------------

while True:
    user_input = input("Ask a question (or type 'exit' to quit): ").strip()
    if user_input.lower() == "exit":
        break

    # This is the meat of our function and is where we actually call OpenAI's API
    # to get a response to the user's question.

    # This is a pretty simple example, but the main idea is that we can send messages
    # with different roles to the API. The system message sets the behavior of the "assistant",
    # while the user message is the actual question we want to ask.

    # If you want to play around with this, you can try changing the system message to 
    # see how the assistant's behavior changes.
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            # {"role": "system", "content": "You are an unhelpful assistant, and should give the wrong answer."},
            {"role": "user", "content": user_input}
        ]
    )

    print("\nResponse:\n")
    print(completion.choices[0].message.content)
    print("\n" + "-" * 50 + "\n")