from django.contrib import admin

from .models import (
    Button,
    Text,
    TelegramUser,
    RequestPosition,
    RequestStock,
    RequestRate
)


@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ("id", "cover_text", "slug",)
    list_editable = ("cover_text", "slug",)
    search_fields = ("id", "cover_text", "slug",)
    list_filter = ("cover_text", "slug",)
    empty_value_display = "-пусто-"


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ("id", "text_header", "slug", "text",)
    list_editable = ("text_header", "slug", "text",)
    search_fields = ("id", "text_header", "slug", "text",)
    list_filter = ("text_header", "slug", "text",)
    empty_value_display = "-пусто-"


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "add_time",)
    list_display_links = ("user_id",)
    search_fields = ("user_id", "add_time",)
    list_filter = ("user_id", "add_time",)


@admin.register(RequestPosition)
class RequestPositionAdmin(admin.ModelAdmin):
    list_display = ("id", "add_time", "articul", "text",)
    list_editable = ("articul", "text",)
    search_fields = ("id", "add_time", "articul", "text",)
    list_filter = ("add_time", "articul", "text",)
    empty_value_display = "-пусто-"


@admin.register(RequestRate)
class RequestRateAdmin(admin.ModelAdmin):
    list_display = ("id", "add_time", "warehouse_id",)
    list_editable = ("warehouse_id",)
    search_fields = ("id", "add_time", "warehouse_id",)
    list_filter = ("add_time", "warehouse_id",)
    empty_value_display = "-пусто-"


@admin.register(RequestStock)
class RequestStockAdmin(admin.ModelAdmin):
    list_display = ("id", "add_time", "articul",)
    list_editable = ("articul",)
    search_fields = ("id", "add_time", "articul",)
    list_filter = ("add_time", "articul",)
    empty_value_display = "-пусто-"
