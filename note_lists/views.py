from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from urllib.parse import quote

from openai_utils import generate_openai_text
from .models import NoteList, Note


def get_note_lists(request):
    note_lists = NoteList.objects.all()
    return render(request, 'note_lists.html', {'note_lists': note_lists})


@require_POST
def add_note_list(request):
    title = request.POST.get('title')
    NoteList.objects.create(title=title)
    return redirect('get_note_lists')


def get_note_list(request, note_list_id):
    note_list = get_object_or_404(NoteList, id=note_list_id)
    report = request.GET.get('report', '')

    context = {
        'note_list': note_list,
        'report': report,
    }

    return render(request, 'note_list.html', context)


def delete_note_list(request, note_list_id):
    note_list = get_object_or_404(NoteList, id=note_list_id)
    note_list.delete()
    return redirect('get_note_lists')


@require_POST
def add_note(request, note_list_id):
    title = request.POST.get('title')
    text = request.POST.get('text')
    note_list = get_object_or_404(NoteList, id=note_list_id)
    Note.objects.create(title=title, text=text, note_list=note_list)
    return redirect('get_note_list', note_list_id=note_list_id)


def delete_note(request, note_list_id, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('get_note_list', note_list_id=note_list_id)


@require_POST
def generate_report(request, note_list_id):
    note_list = get_object_or_404(NoteList, id=note_list_id)
    report = generate_report_using_openai(note_list)
    encoded_report = quote(report)
    return redirect(f"{reverse('get_note_list', args=[note_list_id])}?report={encoded_report}")


def generate_report_using_openai(note_list):
    system_prompt = \
        'Generate a well-structured and concise report based on the provided notes.' \
        'Detect the language used in the notes and use the same language for the report.' \
        'The report should NOT contain the notes itself but should summarize the main points and give a conclusion.'\
        'You will receive the following parameters:' \
        '- note_list_title' \
        '- notes_text: A list of notes, each with a title and a text, formatted as (title: ..., text: ...)'

    notes = note_list.notes.all()
    notes_text = ",".join([f"(title: {note.title}, text: {note.text})" for note in notes])

    user_prompt = f"Generate a report. note_list_title: {note_list.title}, notes_text: {notes_text}"

    return generate_openai_text(system_prompt, user_prompt)
