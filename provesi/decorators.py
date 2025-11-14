from functools import wraps
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib import messages
from provesi.auth0backend import getRole
# from provesi.security import is_blocked, block_and_log

def _get_role_cached(request):
    if not request.user or not request.user.is_authenticated:
        return None
    role = request.session.get('auth0_role')
    if role:
        return role
    try:
        role = getRole(request)  # no modificar auth0backend
        if role:
            request.session['auth0_role'] = role  # cache simple en sesión
        return role
    except Exception:
        return None

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)

            wants_json = (
                'application/json' in (request.headers.get('accept','').lower()) or
                request.headers.get('x-requested-with') == 'XMLHttpRequest'
            )

            role = _get_role_cached(request)

            if role is None:
                if wants_json:
                    return JsonResponse({"success": False, "message": "Rol no disponible."}, status=403)
                return HttpResponseForbidden("Rol no disponible.")

            if role in allowed_roles:
                return view_func(request, *args, **kwargs)

            if wants_json:
                return JsonResponse({"success": False, "message": "No tiene permisos para realizar esa acción."}, status=403)
            return HttpResponseForbidden("No tiene permisos para realizar esa acción.")
        return _wrapped
    return decorator