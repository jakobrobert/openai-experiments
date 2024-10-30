from openai import OpenAI
from dotenv import load_dotenv
import os


def generate_openai_text(system_prompt, user_prompt):
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return completion.choices[0].message.content
