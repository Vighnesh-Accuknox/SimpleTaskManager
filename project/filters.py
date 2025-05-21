import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    deadline = django_filters.DateTimeFilter(field_name='deadline', lookup_expr='lte')
    project = django_filters.NumberFilter(field_name='project__id', lookup_expr='exact')

    class Meta:
        model = Task
        fields = ['status', 'deadline', 'project']
