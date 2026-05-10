from rest_framework import viewsets, permissions, filters
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TaskFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Move the stats action here, because it calculates stats for a Project!
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        project = self.get_object()  # Fetches the specific project instance
        tasks = project.tasks.all()  # Fetches all tasks associated with this project
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)


        total_tasks = tasks.count()
        done_tasks = tasks.filter(status="done").count()

        return Response({
            "project": project.name,
            "total": total_tasks,
            "todo": tasks.filter(status="todo").count(),
            "in_progress": tasks.filter(status="in_progress").count(),
            "done": done_tasks,
            "high_priority": tasks.filter(priority="high").count(), 
            "overdue": tasks.filter(
                due_date__lt=today,
                status__in=["todo", "in_progress"]
            ).count(),
            "completion_pct": round(
                (done_tasks / total_tasks * 100) if total_tasks > 0 else 0, 
                1
            ),
        })

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_class = TaskFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)