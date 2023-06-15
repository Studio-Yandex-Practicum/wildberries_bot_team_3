from django.db import models
from tinymce.models import HTMLField


class Text(models.Model):
    id = models.AutoField(primary_key=True)
    text_header = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    text = HTMLField()
    buttons = models.ManyToManyField('Button', related_name='text')

    def __str__(self):
        return self.text_header


class Button(models.Model):
    id = models.AutoField(primary_key=True)
    cover_text = models.CharField(max_length=255)
    slug = models.ForeignKey(
        Text,
        on_delete=models.SET_NULL,
        related_name='button',
        null=True
    )

    def __str__(self):
        return self.cover_text
