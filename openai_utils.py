import openai
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


def generate_openai_image(prompt):
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    client = OpenAI(api_key=api_key)

    try:
        images = client.images.generate(
            model='dall-e-3',
            prompt=prompt,
            n=1,
            size='1024x1024',
            response_format='url'
        )

        return {'image': images.data[0], 'error_message': None}
    except openai.BadRequestError as e:
        return {'image': None, 'error_message': e.message}
