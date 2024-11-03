from django.shortcuts import render
from django.views.decorators.http import require_POST


def image_generator(request):
    # TODO Get params & send to template by context
    return render(request, 'image_generator.html')


@require_POST
def generate_image():
    # TODO Implement image generation
    return None
