import logging
from django.core.cache import cache
from django.conf import settings
from provesi.auth0backend import getRole

logger = logging.getLogger('security')
BLOCK_TTL_SECONDS = 60

def _client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

def _user_id(request):
    if request.user and request.user.is_authenticated:
        return f"user:{request.user.id}"
    return "anon"

def is_blocked(request):
    uid = _user_id(request)
    ip = _client_ip(request)
    return cache.get(f"block:{uid}") or cache.get(f"block:ip:{ip}")

def block_and_log(request, event, pedido_id=None, reason=None, extra=None):
    uid = _user_id(request)
    ip = _client_ip(request)
    role = None
    try:
        if request.user and request.user.is_authenticated:
            role = getRole(request)
    except Exception:
        role = None

    cache.set(f"block:{uid}", True, BLOCK_TTL_SECONDS)
    cache.set(f"block:ip:{ip}", True, BLOCK_TTL_SECONDS)

    logger.warning(
        "SECURITY event=%s user=%s ip=%s role=%s pedido_id=%s reason=%s extra=%s",
        event, uid, ip, role, pedido_id, reason, extra
    )