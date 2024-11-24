from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

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

    report = request.session.get('report', '')
    error_message = request.session.get('error_message', '')

    context = {
        'note_list': note_list,
        'report': report,
        'error_message': error_message
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
def generate_notes(request, note_list_id):
    note_list = get_object_or_404(NoteList, id=note_list_id)
    description = request.POST.get('description')
    num_notes = request.POST.get('num_notes')

    notes_json, error_message = generate_notes_json_using_openai(note_list.title, description, num_notes)
    # TODO create notes objects from json, store into database
    print(f'notes_json: {notes_json}')

    if error_message:
        request.session['error_message'] = error_message

    return redirect('get_note_list', note_list_id=note_list_id)


@require_POST
def generate_report(request, note_list_id):
    note_list = get_object_or_404(NoteList, id=note_list_id)

    report, error_message = generate_report_using_openai(note_list)

    if report:
        request.session['report'] = report
        request.session['error_message'] = None
    else:
        request.session['report'] = None
        request.session['error_message'] = error_message

    return redirect('get_note_list', note_list_id=note_list_id)


def generate_report_using_openai(note_list):
    # TODO add line breaks here as well
    system_prompt = \
        'Generate a well-structured and concise report based on the provided notes.' \
        'Detect the language used in the notes and use the same language for the report.' \
        'The report should NOT contain the notes itself but should summarize the main points and give a conclusion.'\
        'You will receive the following parameters:' \
        '- note_list_title' \
        '- notes_text: A list of notes, each with a title and a text, formatted as (title: ..., text: ...)'

    notes = note_list.notes.all()
    notes_text = ','.join([f'(title: {note.title}, text: {note.text})' for note in notes])

    user_prompt = f'Generate a report. note_list_title: {note_list.title}, notes_text: {notes_text}'

    return generate_openai_text(system_prompt, user_prompt)


def generate_notes_json_using_openai(note_list_title, description, num_notes):
    system_prompt = (
        'You are a helpful assistant that generates notes based on the given parameters.\n'
        'The response should be in JSON format, where each note is an object with title and text.\n'
        'The parameters you will receive are:\n'
        '- note_list_title: The title of the note list\n'
        '- description: A description to guide the content of the notes\n'
        '- num_notes: The number of notes to generate\n'
    )

    user_prompt = (
        'Generate the notes.\n'
        f'note_list_title: {note_list_title}, description: {description}, num_notes: {num_notes}'
    )

    return generate_openai_text(system_prompt, user_prompt)
