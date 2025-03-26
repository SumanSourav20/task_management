from rest_framework import serializers
from .models import Status, Task, Project, Comment
from .validators import hex_color_validator
from accounts.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name()
    

class StatusSerializer(serializers.ModelSerializer):
    color = serializers.CharField(
        max_length=7, 
        validators=[hex_color_validator],
    )
    class Meta:
        model = Status
        fields = ['id', 'name', 'color']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user.profile
        return super().create(validated_data)
    
class CommentSerializer(serializers.ModelSerializer):
    created_by = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'updated_at', 'created_by']
        read_only_fields = ['created_at','updated_at',]

class TaskSerializer(serializers.ModelSerializer):
    status_display = StatusSerializer(read_only=True)
    assignees = ProfileSerializer(many=True,read_only=True)
    comments_count = serializers.SerializerMethodField()
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'priority_display', 'due_date',
                'status', 'status_display', 'project', 'assignees', 'comments_count']
    
    def get_comments_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user.profile
        return super().create(validated_data)
    
    
class TaskDetailSerializer(TaskSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['comments', 'created_by', 'created_at',]

class ProjectSerializer(serializers.ModelSerializer):
    created_by = ProfileSerializer(read_only=True)
    tasks_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'closed', 'created_by', 'tasks_count']
        read_only_fields = ['created_at']

    def get_tasks_count(self, obj):
        return obj.tasks.count()

class ProjectDetailSerializer(ProjectSerializer):
    tasks = serializers.SerializerMethodField(read_only=True)
    
    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ['tasks']
    
    def get_tasks(self, obj):
        return TaskSerializer(obj.tasks.all(), many=True).data

class TaskAssignSerializer(serializers.Serializer):
    profile_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True
    )