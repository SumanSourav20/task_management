from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet, DateFilter, ModelMultipleChoiceFilter
from rest_framework.pagination import PageNumberPagination

from .models import Project, Status, Task, Comment
from .serializers import (
    TaskSerializer, 
    TaskDetailSerializer,
    StatusSerializer, 
    CommentSerializer,
)
from accounts.models import Profile

from drf_spectacular.utils import extend_schema, OpenApiExample

class SetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_pages_size = 1000

class TaskFilter(FilterSet):
    due_date_min = DateFilter(field_name="due_date", lookup_expr="gte")
    due_date_max = DateFilter(field_name="due_date", lookup_expr="lte")
    created_date_min = DateFilter(field_name="created_at",lookup_expr="gte")
    created_date_max = DateFilter(field_name="created_at",lookup_expr="lte")

    assignees = ModelMultipleChoiceFilter(
        field_name="assignees",
        queryset=Profile.objects.all(),
        conjoined=False
    )
    
    assignees_all = ModelMultipleChoiceFilter(
        field_name="assignees",
        queryset=Profile.objects.all(),
        conjoined=True
    )

    class Meta:
        model = Task
        fields = {
            'status': ['exact'],
            'priority': ['exact'],
        }

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends=[DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "created_at"]
    
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
    
    @extend_schema(
        description="Assign users to a task",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'profile_ids': {
                        'type': 'array',
                        'items': {'type': 'integer'}
                    }
                },
                'required': ['profile_ids']
            }
        },
        responses={
            200: TaskDetailSerializer,
        },
        examples=[
            OpenApiExample(
                name='Valid Assignment Request',
                value={'profile_ids': [1, 2, 3]},
                request_only=True,
            ),
        ]
    )
        
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None, project_pk=None):
        task = self.get_object()
        
        profile_ids = request.data.get('profile_ids', [])
        
        if not profile_ids:
            return Response(
                {"detail": "Profile IDs are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profiles = Profile.objects.filter(id__in=profile_ids)
        if not profiles.exists():
            return Response(
                {"detail": "No valid profiles found with the provided IDs"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.assignees.add(*profiles)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)
    
    @extend_schema(
        description="Unassign users from a task",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'profile_ids': {
                        'type': 'array',
                        'items': {'type': 'integer'}
                    }
                },
                'required': ['profile_ids']
            }
        },
        responses={
            200: TaskDetailSerializer,
        },
        examples=[
            OpenApiExample(
                name='Valid Unassignment Request',
                value={'profile_ids': [1, 2, 3]},
                request_only=True,
            ),
        ]
    )
    @action(detail=True, methods=['post'])
    def unassign(self, request, pk=None, project_pk=None):
        task = self.get_object()
        
        profile_ids = request.data.get('profile_ids', [])
        
        if not profile_ids:
            return Response(
                {"detail": "Profile IDs are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profiles = Profile.objects.filter(id__in=profile_ids)
        task.assignees.remove(*profiles)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)


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
