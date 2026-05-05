from django.contrib import admin
from .models import Project, Task

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "created_at"]
    search_fields = ["name", "owner__username"]
    list_filter = ["created_at"]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "project","status", "priority", "due_date"]
    list_filter = ["status", "priority", "due_date"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]

    