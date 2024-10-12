from django.shortcuts import render, redirect, get_object_or_404
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


def note_list(request, pk):
    note_list = get_object_or_404(NoteList, pk=pk)
    notes = note_list.notes.all()
    return render(request, 'note_list.html', {'note_list_title': note_list.title, 'notes': notes})