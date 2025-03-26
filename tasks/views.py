from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Project, Status, Task, Comment
from .serializers import (
    ProjectSerializer, ProjectDetailSerializer,
    TaskSerializer, TaskDetailSerializer,
    StatusSerializer, CommentSerializer,
    ProfileSerializer,
    TaskAssignSerializer
)
from accounts.models import Profile


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile)
    
    @action(detail=True)
    def tasks(self, request, pk=None):
        project = self.get_object()
        tasks = project.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Task.objects.all()
        project_id = self.kwargs.get('project_pk')
        profile_id = self.request.query_params.get('profile_id')
        
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        
        if profile_id is not None:
            queryset = queryset.filter(assignees__id=profile_id)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskSerializer
        
    @action(detail=False, methods=['get'])
    def by_profile(self, request, project_pk=None):
        profile_id = request.query_params.get('profile_id')
        
        if not profile_id:
            return Response(
                {"detail": "Profile ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        queryset = self.get_queryset().filter(assignees__id=profile_id)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    
class TaskAssignView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        
        serializer = TaskAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile_ids = serializer.validated_data.get('profile_ids', [])
        
        profiles = Profile.objects.filter(id__in=profile_ids)
        if not profiles.exists() and profile_ids:
            return Response(
                {"detail": "No valid users provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.assignees.add(*profiles)
        detail_serializer = TaskDetailSerializer(task)
        return Response(detail_serializer.data)


class TaskUnassignView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        
        serializer = TaskAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile_ids = serializer.validated_data.get('profile_ids', [])
        
        profiles = Profile.objects.filter(id__in=profile_ids)
        task.assignees.remove(*profiles)
        detail_serializer = TaskDetailSerializer(task)
        return Response(detail_serializer.data)


class StatusViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        if task_id:
            return Comment.objects.filter(task_id=task_id)
        return Comment.objects.none()
    
    def create(self, request, *args, **kwargs):
        task_id = self.kwargs.get('task_pk')
        
        if task_id:
            task = get_object_or_404(Task, id=task_id)
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    task=task,
                    created_by=request.user.profile
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(
                {"detail": "Task ID is required in the URL"},
                status=status.HTTP_400_BAD_REQUEST
            )
