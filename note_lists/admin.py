from django.contrib import admin

from .models import NoteList
from .models import Note

admin.site.register(NoteList)
admin.site.register(Note)
