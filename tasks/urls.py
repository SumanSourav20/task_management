from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, TaskViewSet, StatusViewSet, CommentViewSet, TaskAssignView, TaskUnassignView

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'statuses', StatusViewSet, basename='status')
router.register(r'tasks/(?P<task_pk>\d+)/comments', CommentViewSet, basename='task-comments')

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'tasks', TaskViewSet, basename='project-tasks')

tasks_router = routers.NestedSimpleRouter(projects_router, r'tasks', lookup='task')
tasks_router.register(r'comments', CommentViewSet, basename='task-comments')

router.register(r'tasks', TaskViewSet, basename='task')

standalone_tasks_router = routers.NestedSimpleRouter(router, r'tasks', lookup='task')
standalone_tasks_router.register(r'comments', CommentViewSet, basename='standalone-task-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(tasks_router.urls)),
    path('', include(standalone_tasks_router.urls)),
    path('tasks/<int:pk>/assign/', TaskAssignView.as_view(), name='task-assign'),
    path('tasks/<int:pk>/unassign/', TaskUnassignView.as_view(), name='task-unassign'),
]