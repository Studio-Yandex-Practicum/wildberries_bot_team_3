from django.db import models


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


class PositionSubscription(Request):
    user_id = models.IntegerField(unique=False)
    articul = models.IntegerField(unique=True)
    text = models.CharField(max_length=255)
    frequency = models.IntegerField()
    position = models.IntegerField(default=0)

    def __str__(self):
        return f"Артикул: {self.articul}, текст: {self.text}, периодичность: {self.frequency}, позиция: {self.position}"