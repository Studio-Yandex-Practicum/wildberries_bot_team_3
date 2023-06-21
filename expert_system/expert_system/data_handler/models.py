from django.db import models
from tinymce.models import HTMLField


class IdModel(models.Model):
    """Абстрактная модель. Добавляет id."""
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    add_time = models.DateTimeField(
        verbose_name='Время добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True


class Text(IdModel):
    """Модель текстов к кнопкам бота."""
    text_header = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    text = HTMLField()
    buttons = models.ManyToManyField('Button', related_name='text', blank=True)

    def __str__(self):
        return self.text_header


class Button(IdModel):
    """Модель кнопок бота."""
    cover_text = models.CharField(max_length=255)
    slug = models.ForeignKey(
        Text,
        on_delete=models.SET_NULL,
        related_name='button',
        null=True
    )

    def __str__(self):
        return self.cover_text


class TelegramUser(IdModel, CreatedModel):
    """Модель телеграмм-пользователя подписанного на бота."""
    user_id = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f'Пользователь {self.user_id}'


class RequestPosition(IdModel, CreatedModel):
    """Модель запроса позиции на сайте."""
    articul = models.IntegerField()
    text = models.CharField(max_length=255)

    def __str__(self):
        return f'Артикул: {self.articul}, текст: {self.text}'


class RequestStock(IdModel, CreatedModel):
    """Модель запроса остатков."""
    articul = models.IntegerField()

    def __str__(self):
        return f'Артикул: {self.articul}'


class RequestRate(IdModel, CreatedModel):
    """Модель коэффициентов приемки."""
    warehouse_id = models.IntegerField()

    def __str__(self):
        return f'Warehouse_id: {self.warehouse_id}'
