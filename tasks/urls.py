from django.urls import path, include
from rest_framework_nested import routers
from tasks.views import TaskViewSet, StatusViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'statuses', StatusViewSet, basename='status')
router.register(r'tasks/(?P<task_pk>\d+)/comments', CommentViewSet, basename='task-comments')

router.register(r'tasks', TaskViewSet, basename='task')

tasks_router = routers.NestedSimpleRouter(router, r'tasks', lookup='task')
tasks_router.register(r'comments', CommentViewSet, basename='standalone-task-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tasks_router.urls))
]