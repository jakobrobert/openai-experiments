from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import NoteList


def note_lists(request):
    note_lists = NoteList.objects.all()
    return render(request, 'note_lists.html', {'note_lists': note_lists})


@require_POST
def add_note_list(request):
    title = request.POST.get('title')
    NoteList.objects.create(title=title)
    return redirect('note_lists')
