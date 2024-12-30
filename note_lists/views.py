import json

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

    generate_notes_description = request.session.get('generate_notes_description', '')
    generate_notes_num_notes = request.session.get('generate_notes_num_notes', '1')
    report_language = request.session.get('report_language', '')
    report = request.session.pop('report', '')
    error_message = request.session.pop('error_message', '')

    context = {
        'note_list': note_list,
        'generate_notes_description': generate_notes_description,
        'generate_notes_num_notes': generate_notes_num_notes,
        'report_language': report_language,
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


def clear_notes(request, note_list_id):
    note_list = get_object_or_404(NoteList, id=note_list_id)
    note_list.notes.all().delete()
    return redirect('get_note_list', note_list_id=note_list_id)


@require_POST
def generate_notes(request, note_list_id):
    note_list = get_object_or_404(NoteList, id=note_list_id)
    description = request.POST.get('description')
    num_notes = request.POST.get('num_notes')

    request.session['generate_notes_description'] = description
    request.session['generate_notes_num_notes'] = num_notes

    notes_json_str, error_message = generate_notes_json_using_openai(note_list.title, description, num_notes)

    if error_message:
        request.session['error_message'] = error_message
    else:
        notes_data = json.loads(notes_json_str)
        save_notes_to_database(notes_data, note_list)

    return redirect('get_note_list', note_list_id=note_list_id)


@require_POST
def generate_report(request, note_list_id):
    note_list = get_object_or_404(NoteList, id=note_list_id)
    language = request.POST.get('report_language')

    request.session['report_language'] = language

    report, error_message = generate_report_using_openai(note_list, language)

    if report:
        request.session['report'] = report
        request.session['error_message'] = None
    else:
        request.session['report'] = None
        request.session['error_message'] = error_message

    return redirect('get_note_list', note_list_id=note_list_id)


def generate_report_using_openai(note_list, language):
    system_prompt = (
        'Generate a report based on the provided notes. '
        'The report should provide a high-level analysis, integrating the notes into a coherent narrative. '
        'It should not simply repeat the notes verbatim, but rather synthesize and interpret the key insights. '
        'Highlight any patterns, trends, or unique observations that emerge from the notes. '
        'Do NOT include the note list title. '
        'The output should be in HTML format and might contain several headings and paragraphs. '
        'The max heading level should be h3.'
        'You will receive the following parameters:\n'
        '- language: e.g. German, English, etc.\n'
        '- note_list_title\n'
        '- notes_text: A list of notes, each with a title and a text, formatted as (title: ..., text: ...)\n'
    )

    notes = note_list.notes.all()
    notes_text = ','.join([f'(title: {note.title}, text: {note.text})' for note in notes])

    user_prompt = \
        'Generate a report. ' \
        f'language: {language}, note_list_title: {note_list.title}, notes_text: {notes_text}'

    return generate_openai_text(system_prompt, user_prompt)


def generate_notes_json_using_openai(note_list_title, description, num_notes):
    system_prompt = (
        'Generates notes based on the given parameters.\n'
        'Each note is an object with title and text.\n'
        'The response must be a raw JSON array containing the notes, without any wrapping object.\n'
        'The parameters you will receive are:\n'
        '- note_list_title: The title of the note list\n'
        '- description: A description to guide the content of the notes\n'
        '- num_notes: The number of notes to generate\n'
    )

    user_prompt = (
        'Generate the notes.\n'
        f'note_list_title: {note_list_title}, description: {description}, num_notes: {num_notes}\n'
    )

    return generate_openai_text(system_prompt, user_prompt)


def save_notes_to_database(notes_data, note_list):
    notes = []

    for note_data in notes_data:
        notes.append(Note(title=note_data['title'], text=note_data['text'], note_list=note_list))

    Note.objects.bulk_create(notes)
