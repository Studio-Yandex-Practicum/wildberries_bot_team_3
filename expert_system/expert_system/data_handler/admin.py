from django.contrib import admin

from .models import Button, Text, TelegramUser


@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cover_text",
        "slug",
    )
    list_editable = (
        "cover_text",
        "slug",
    )
    search_fields = (
        "id",
        "cover_text",
        "slug",
    )
    list_filter = (
        "cover_text",
        "slug",
    )
    empty_value_display = "-пусто-"


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "text_header",
        "slug",
        "text",
    )
    list_editable = (
        "text_header",
        "slug",
        "text",
    )
    search_fields = (
        "id",
        "text_header",
        "slug",
        "text",
    )
    list_filter = (
        "text_header",
        "slug",
        "text",
    )
    empty_value_display = "-пусто-"


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
    )
    list_editable = ("user_id",)
    search_fields = ("user_id",)
    list_filter = ("user_id",)
