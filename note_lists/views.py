from django.shortcuts import render


def note_lists(request):
    return render(request, 'note_lists.html')


def add_note_list(request):
    pass
