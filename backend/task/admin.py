from django.contrib import admin

from task.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "user",
        "status",
        "priority",
        "due_date",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
    )

    search_fields = (
        "title",
        "description",
        "user__email",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )