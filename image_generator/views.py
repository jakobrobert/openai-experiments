from django.shortcuts import render
from django.views.decorators.http import require_POST

from utils import generate_openai_image


def image_generator(request):
    # TODO Get params & send to template by context
    return render(request, 'image_generator.html')


@require_POST
def generate_image(request):
    prompt = request.POST.get('prompt')

    image = generate_openai_image(prompt)

    print(f'revised_prompt: {image.revised_prompt}')
    print(f'url: {image.url}')

    return None
