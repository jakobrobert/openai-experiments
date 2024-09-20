from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv("django_project/.env")
API_KEY = os.getenv("API_KEY")

client = OpenAI(
    api_key=API_KEY
)


# TODO Create method to generate motivational quotes. Add params language, tone, verbosity.
#  Maybe also how well performed in recent days. For the params, add a number to indicate intensity.
def generate_motivational_quote(language, tone, verbosity):
    system_prompt = \
        "You are a life coach." \
        "Your task is to generate motivational quotes based on the following parameters: language, tone and verbosity." \
        "The language can have e.g. following values: English, German, etc."\
        "The tone ranges from 1 (very aggressive and insulting) to 5 (very polite, careful and empathetic)." \
        "The verbosity ranges from 1 (very brief) to 5 (very detailed)."

    user_prompt = f"Generate a motivational quote. language: {language}, tone: {tone}, verbosity: {verbosity}"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    while True:
        print("Please enter the following parameters to generate a motivational quote:")

        language = input("Language (e.g. German, English, etc.): ")
        tone = int(input("Tone (1 - 5): "))
        verbosity = int(input("Verbosity (1 - 5): "))

        quote = generate_motivational_quote(language, tone, verbosity)
        print(f"Quote: {quote}\n")
