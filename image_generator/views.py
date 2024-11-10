from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from openai_utils import generate_openai_image


def image_generator(request):
    prompt = request.session.get('prompt', '')
    revised_prompt = request.session.get('revised_prompt', '')
    image_url = request.session.get('image_url', '')

    context = {
        'prompt': prompt,
        'revised_prompt': revised_prompt,
        'image_url': image_url
    }

    return render(request, 'image_generator.html', context)


@require_POST
def generate_image(request):
    prompt = request.POST.get('prompt')

    image, error_message = generate_openai_image(prompt)

    if image:
        request.session['prompt'] = prompt
        request.session['revised_prompt'] = image.revised_prompt
        request.session['image_url'] = image.url
    else:
        request.session['error_message'] = error_message
        print(error_message)

    return redirect('image_generator')
