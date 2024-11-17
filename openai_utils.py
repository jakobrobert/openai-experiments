import openai
from openai import OpenAI
from dotenv import load_dotenv
import os


def generate_openai_text(system_prompt, user_prompt):
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    client = OpenAI(api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        return completion.choices[0].message.content, None
    except openai.BadRequestError as e:
        return None, e.body['message']
    except Exception:
        return None, 'Unknown error'


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

        return images.data[0], None
    except openai.BadRequestError as e:
        return None, e.body['message']
    except Exception:
        return None, 'Unknown error'
