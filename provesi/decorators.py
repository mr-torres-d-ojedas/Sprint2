from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from provesi.auth0backend import getRole
from provesi.security import is_blocked, block_and_log

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if is_blocked(request):
                # Revoca inmediatamente (menos de 1s) tras detección previa
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"success": False, "message": "Acceso revocado temporalmente."}, status=403)
                messages.error(request, "Acceso revocado temporalmente.")
                return redirect('lista_pedidos')

            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)

            def wants_json():
                accept = (request.headers.get('accept') or '').lower()
                xrw = request.headers.get('x-requested-with') == 'XMLHttpRequest'
                ctype = (request.headers.get('content-type') or '').lower()
                return 'application/json' in accept or xrw or 'application/json' in ctype

            try:
                role = getRole(request)
            except Exception:
                block_and_log(request, event="AUTH_ROLE_ERROR", reason="no_role_claim")
                if wants_json():
                    return JsonResponse({"success": False, "message": "No tiene permisos para realizar esa acción."}, status=403)
                messages.error(request, "No tiene permisos para realizar esa acción.")
                return redirect('lista_pedidos')

            if role in allowed_roles:
                return view_func(request, *args, **kwargs)

            block_and_log(request, event="UNAUTHORIZED_ROLE", reason=f"role={role}, allowed={allowed_roles}")
            if wants_json():
                return JsonResponse({"success": False, "message": "No tiene permisos para realizar esa acción."}, status=403)
            messages.error(request, "No tiene permisos para realizar esa acción.")
            return redirect('lista_pedidos')
        return _wrapped
    return decorator