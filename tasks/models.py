from django.db import models
from accounts.models import Profile

class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_projects')
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
        
class Status(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_statuses')
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255, blank=True, null=True)


class Task(models.Model):
    PRIORITY_LOW = 'L'
    PRIORITY_MEDIUM = 'M'
    PRIORITY_HIGH = 'H'
    PRIORITY_CHOICES = {
        PRIORITY_LOW : 'Low',
        PRIORITY_MEDIUM : 'Medium',
        PRIORITY_HIGH : 'High',
    }

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=PRIORITY_LOW)
    assignee = models.ManyToManyField(Profile, related_name='assigned_tasks', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    duedate = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_tasks')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
