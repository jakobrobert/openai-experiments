from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")

client = OpenAI(
    api_key=API_KEY
)


# TODO Create method to generate motivational quotes. Add params language, tone, verbosity.
#  Maybe also how well performed in recent days. For the params, add a number to indicate intensity.
def send_prompt(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    while True:
        user_input = input("You: ")

        # TODO adjust input handling. user should input the different parameters, then show the motivational quote.
        if user_input.lower() in ["exit"]:
            break

        response = send_prompt(user_input)
        print(f"ChatGPT: {response}")
