from django.db import models

class Hawker(models.Model):
    name = models.CharField('Name', max_length=255)

    created = models.DateTimeField('Created', auto_now_add=True)
    changed = models.DateTimeField('Changed', auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    