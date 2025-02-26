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
        break  # Exit loop if user types 'exit'

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    print("\nResponse:\n")
    print(completion.choices[0].message.content)
    print("\n" + "-" * 50 + "\n")