from django.db import models


class NoteList(models.Model):
    title = models.CharField(max_length=255)


class Note(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    note_list = models.ForeignKey(NoteList, on_delete=models.CASCADE, related_name='notes')
