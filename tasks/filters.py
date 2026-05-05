import django_filters
from .models import Project, Task

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)
    due_date_after = django_filters.DateTimeFilter(field_name="due_date", lookup_expr="gte")
    due_date_before = django_filters.DateTimeFilter(field_name="due_date", lookup_expr="lte")

    class Meta:
        model = Task
        fields = {            
            "status": ["exact"],
            "priority": ["exact"],
            "project": ["gte", "lte"],
            "assigned_to": ["exact"]
        }


