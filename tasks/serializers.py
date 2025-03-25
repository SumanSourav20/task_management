from rest_framework import serializers
from .models import Status, Task, Project, Comment
from .validators import hex_color_validator
from accounts.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        models = Profile
        fields = ['id', 'full_name']

class StatusSerialzier(serializers.ModelSerializer):
    color = serializers.CharField(
        max_length=7, 
        validators=[hex_color_validator],
    )
    class Meta:
        model = Status
        fields = ['id', 'name', 'color']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['profile'] = user.profile
        return super().create(validated_data)
    
class CommentSerializer(serializers.ModelSerializer):
    created_by = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'updated_at', 'created_by']
        read_only_fields = ['updated_at']

class TaskSerializer(serializers.ModelSerializer):
    status = StatusSerialzier(read_only=True)
    assignees = ProfileSerializer(many=True,read_only=True)
    comments_count = serializers.SerializerMethodField()
    priority_display = serializers.CharField(source='get_priority_display')
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'priority', 'priority_display', 'duedate',
                'status', 'project', 'assignees']
    
    def get_comments_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user.profile
        return super().create(validated_data)
    
    
class TaskDetailSerializer(TaskSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['comments']

