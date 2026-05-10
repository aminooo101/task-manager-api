# tasks/serializers.py
from rest_framework import serializers
from .models import Project, Task

class ProjectSerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()

    class Meta:
        model  = Project
        fields = ["id", "name", "description", "created_at", "task_count"]  # ← campos de Project
        read_only_fields = ["id", "created_at"]

    def get_task_count(self, obj):
        return obj.tasks.count()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Task
        fields = ["id", "project", "title", "status", "priority",
                  "due_date", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]