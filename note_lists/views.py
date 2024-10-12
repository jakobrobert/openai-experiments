from django.shortcuts import render

from .models import NoteList


def note_lists(request):
    note_lists = NoteList.objects.all()
    return render(request, 'note_lists.html', {'note_lists': note_lists})


def add_note_list(request):
    pass
