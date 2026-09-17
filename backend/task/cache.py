import hashlib
import json
from uuid import uuid4

from django.conf import settings
from django.core.cache import cache


CACHE_VERSION_KEY = "tasks:cache-version:user:{user_id}"


def get_task_cache_version(user_id):
    key = CACHE_VERSION_KEY.format(user_id=user_id)

    return cache.get_or_set(
        key,
        uuid4().hex,
        timeout=None,
    )


def build_task_list_cache_key(
    *,
    user_id,
    query_params,
):
    version = get_task_cache_version(user_id)

    relevant_params = {
        "status": query_params.get("status", ""),
        "priority": query_params.get("priority", ""),
        "search": query_params.get("search", ""),
        "ordering": query_params.get("ordering", ""),
        "page": query_params.get("page", ""),
    }

    normalized_params = json.dumps(
        relevant_params,
        sort_keys=True,
        separators=(",", ":"),
    )

    query_hash = hashlib.sha256(
        normalized_params.encode()
    ).hexdigest()

    return (
        f"tasks:list:"
        f"user:{user_id}:"
        f"version:{version}:"
        f"query:{query_hash}"
    )


def invalidate_task_cache(user_id):
    key = CACHE_VERSION_KEY.format(user_id=user_id)

    cache.set(
        key,
        uuid4().hex,
        timeout=None,
    )


def get_cached_task_list(cache_key):
    return cache.get(cache_key)


def set_cached_task_list(cache_key, data):
    cache.set(
        cache_key,
        data,
        timeout=settings.TASK_CACHE_TIMEOUT,
    )