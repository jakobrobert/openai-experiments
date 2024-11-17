from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from openai_utils import generate_openai_text


def motivational_quotes(request):
    language = request.session.get('language', '')
    tone = request.session.get('tone', '')
    verbosity = request.session.get('verbosity', '')
    quote = request.session.get('quote', '')
    error_message = request.session.get('error_message', '')

    context = {
        'language': language,
        'tone': tone,
        'verbosity': verbosity,
        'quote': quote,
        'error_message': error_message
    }

    return render(request, 'motivational_quotes.html', context)


@require_POST
def generate_quote(request):
    language = request.POST.get('language')
    tone = request.POST.get('tone')
    verbosity = request.POST.get('verbosity')

    request.session['language'] = language
    request.session['tone'] = tone
    request.session['verbosity'] = verbosity

    quote, error_message = generate_quote_using_openai(language, tone, verbosity)

    if quote:
        request.session['quote'] = quote
        request.session['error_message'] = None
    else:
        request.session['quote'] = None
        request.session['error_message'] = error_message

    return redirect('motivational_quotes')


def generate_quote_using_openai(language, tone, verbosity):
    system_prompt = \
        "You are a life coach." \
        "Your task is to generate motivational quotes based on the following parameters: language, tone and verbosity." \
        "The language can have e.g. following values: English, German, etc." \
        "The tone ranges from 1 (very aggressive and insulting) to 5 (very polite, careful and empathetic)." \
        "The verbosity ranges from 1 (very brief) to 5 (very detailed)."

    user_prompt = f"Generate a motivational quote. language: {language}, tone: {tone}, verbosity: {verbosity}"

    return generate_openai_text(system_prompt, user_prompt)
