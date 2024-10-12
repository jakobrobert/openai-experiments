from django.db import models


class NoteList(models.Model):
    title = models.CharField(max_length=255)
