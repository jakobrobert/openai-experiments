from django.shortcuts import render
from django.views.decorators.http import require_POST

from openai import OpenAI
from dotenv import load_dotenv
import os


def index(request):
    return render(request, 'index.html')


@require_POST
def generate_quote(request):
    language = request.POST.get('language')
    tone = request.POST.get('tone')
    verbosity = request.POST.get('verbosity')

    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    client = OpenAI(api_key=api_key)

    quote = generate_motivational_quote(client, language, tone, verbosity)

    context = {
        'language': language,
        'quote': quote
    }

    return render(request, 'index.html', context)


def generate_motivational_quote(client, language, tone, verbosity):
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
