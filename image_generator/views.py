from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from utils import generate_openai_image


def image_generator(request):
    prompt = request.GET.get('prompt', '')
    revised_prompt = request.GET.get('revised_prompt', '')
    image_url = request.GET.get('image_url', '')

    context = {
        'prompt': prompt,
        'revised_prompt': revised_prompt,
        'image_url': image_url
    }

    return render(request, 'image_generator.html', context)


@require_POST
def generate_image(request):
    prompt = request.POST.get('prompt')

    image = generate_openai_image(prompt)

    return redirect(f"{reverse('image_generator')}?prompt={prompt}&revised_prompt={image.revised_prompt}&image_url={image.url}")
