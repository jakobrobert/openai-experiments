from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from utils import generate_openai_text


def motivational_quotes(request):
    language = request.GET.get('language', '')
    tone = request.GET.get('tone', '')
    verbosity = request.GET.get('verbosity', '')
    quote = request.GET.get('quote', '')

    context = {
        'language': language,
        'tone': tone,
        'verbosity': verbosity,
        'quote': quote
    }

    return render(request, 'motivational_quotes.html', context)


@require_POST
def generate_quote(request):
    language = request.POST.get('language')
    tone = request.POST.get('tone')
    verbosity = request.POST.get('verbosity')

    quote = generate_quote_using_openai(language, tone, verbosity)

    return redirect(f"{reverse('motivational_quotes')}?language={language}&tone={tone}&verbosity={verbosity}&quote={quote}")


def generate_quote_using_openai(language, tone, verbosity):
    system_prompt = \
        "You are a life coach." \
        "Your task is to generate motivational quotes based on the following parameters: language, tone and verbosity." \
        "The language can have e.g. following values: English, German, etc." \
        "The tone ranges from 1 (very aggressive and insulting) to 5 (very polite, careful and empathetic)." \
        "The verbosity ranges from 1 (very brief) to 5 (very detailed)."

    user_prompt = f"Generate a motivational quote. language: {language}, tone: {tone}, verbosity: {verbosity}"

    return generate_openai_text(system_prompt, user_prompt)
