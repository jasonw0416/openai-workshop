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
    # GET USER INPUT HERE!

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            # ENTER SYSTEM AND USER MESSAGES HERE!
        ]
    )

    print("\nResponse:\n")
    print(completion.choices[0].message.content)
    print("\n" + "-" * 50 + "\n")