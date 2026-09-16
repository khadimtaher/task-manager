from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from task.models import Task
from task.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self,):
        return Task.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


