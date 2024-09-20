from django.shortcuts import render
from django.views.decorators.http import require_POST


def index(request):
    return render(request, 'index.html')


@require_POST
def generate_quote(request):
    language = request.POST.get('language')
    tone = request.POST.get('tone')
    verbosity = request.POST.get('verbosity')

    # TODO use OpenAI API to generate quote
    quote = f'Generate quote with following params: language: {language}, tone: {tone}, verbosity: {verbosity}'

    return render(request, 'index.html', {'quote': quote})
