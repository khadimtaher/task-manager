import hashlib
import json
from uuid import uuid4
import logging

from django.conf import settings
from django.core.cache import cache
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

CACHE_VERSION_KEY = "tasks:cache-version:user:{user_id}"


def get_task_cache_version(user_id):
    key = CACHE_VERSION_KEY.format(user_id=user_id)
    try:
        # cache.get_or_set can raise exceptions if Redis is down and IGNORE_EXCEPTIONS isn't fully caught
        version = cache.get(key)
        if not version:
            version = uuid4().hex
            cache.set(key, version, timeout=None)
        return version
    except (RedisError, Exception) as e:
        logger.warning(f"Redis down, falling back for cache version: {e}")
        # Fallback return value so app doesn't crash
        return uuid4().hex


def build_task_list_cache_key(*, user_id, query_params):
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
    try:
        cache.set(key, uuid4().hex, timeout=None)
    except (RedisError, Exception) as e:
        logger.warning(f"Redis down during invalidation: {e}")


def get_cached_task_list(cache_key):
    try:
        return cache.get(cache_key)
    except (RedisError, Exception):
        return None  # Treat as cache miss, fallback to DB


def set_cached_task_list(cache_key, data):
    try:
        cache.set(cache_key, data, timeout=getattr(
            settings, 'TASK_CACHE_TIMEOUT', 300))
    except (RedisError, Exception) as e:
        logger.warning(f"Redis down during set cache: {e}")
