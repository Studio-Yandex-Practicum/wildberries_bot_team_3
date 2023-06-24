from django.db import models
from tinymce.models import HTMLField


class Request(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    id = models.AutoField(primary_key=True)
    add_time = models.DateTimeField(
        verbose_name='Время добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True


class Text(models.Model):
    id = models.AutoField(primary_key=True)
    text_header = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    text = HTMLField()
    buttons = models.ManyToManyField('Button', related_name='text', blank=True)

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


class TelegramUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Пользователь {self.user_id}"


class RequestPosition(Request):
    articul = models.IntegerField()
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"Артикул: {self.articul}, текст: {self.text}"


class RequestStock(Request):
    articul = models.IntegerField()

    def __str__(self):
        return f"Артикул: {self.articul}"


class RequestRate(Request):
    warehouse_id = models.IntegerField()

    def __str__(self):
        return f"Warehouse_id: {self.warehouse_id}"
