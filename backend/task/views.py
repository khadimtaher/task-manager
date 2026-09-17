from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from task.models import Task
from task.serializers import TaskSerializer
from task.cache import (
    build_task_list_cache_key,
    get_cached_task_list,
    set_cached_task_list,
    invalidate_task_cache,
)


class TaskViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "priority",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "due_date",
        "title",
        "priority",
        "status",
    ]

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        cache_key = build_task_list_cache_key(
            user_id=request.user.id,
            query_params=request.query_params,
        )

        cached_data = get_cached_task_list(
            cache_key
        )

        if cached_data is not None:
            response = Response(cached_data)
            response["X-Cache"] = "HIT"
            return response

        queryset = self.filter_queryset(
            self.get_queryset()
        )

        page = self.paginate_queryset(
            queryset
        )

        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
            )

            response = self.get_paginated_response(
                serializer.data
            )

            set_cached_task_list(
                cache_key,
                response.data,
            )

            response["X-Cache"] = "MISS"

            return response

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        response_data = serializer.data

        set_cached_task_list(
            cache_key,
            response_data,
        )

        response = Response(
            response_data
        )

        response["X-Cache"] = "MISS"

        return response

    def perform_create(self, serializer):
        task = serializer.save(
            user=self.request.user
        )

        invalidate_task_cache(
            task.user_id
        )

    def perform_update(self, serializer):
        user_id = serializer.instance.user_id

        serializer.save()

        invalidate_task_cache(
            user_id
        )

    def perform_destroy(self, instance):
        user_id = instance.user_id

        instance.delete()

        invalidate_task_cache(
            user_id
        )
