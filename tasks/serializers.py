from rest_framework import serializers
from .models import Status, Task, Project
from .validators import hex_color_validator

class StatusSerialzier(serializers.ModelSerializer):
    color = serializers.CharField(
        max_length=7, 
        validators=[hex_color_validator],
    )
    class Meta:
        model = Status
        fields = ['id', 'created_at', 'created_by', 'name', 'color']
        read_only_field = ['id', 'created_at', 'created_by']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['profile'] = user.profile
        return super().create(validated_data)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
    fields = ['id', 'title', 'priority', 'priority_display', 'duedate', \
                'status', 'status_name', 'created_at', 'project', 'assignees']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user.profile
        return super().create(validated_data)
    
class TaskListSerializer(serializers.ModelSerializer):
    status_name = serializers.SerializerMethodField()
    assignees = serializers.SerializerMethodField()
    priority_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'priority', 'priority_display', 'duedate', 
                  'status', 'status_name', 'created_at', 'project', 'assignees']
        read_only_fields = ['id', 'created_at', 'status_name', 'priority_display', 'assignees']
    
    def get_status_name(self, obj):
        return obj.status.name if obj.status else None
    
    def get_priority_display(self, obj):
        return obj.get_priority_display()
    
    def get_assignees(self, obj):
        return [
            {
                'id': profile.id,
                'name': profile.get_full_name()
            }
            for profile in obj.assignee.all()
        ]