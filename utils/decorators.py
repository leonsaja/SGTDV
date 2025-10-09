from django.shortcuts import redirect
from django.urls import reverse_lazy
from functools import wraps

def has_role_decorator(roles=None, redirect_to_login=None, redirect_url=None):

    roles = roles or []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Se não estiver autenticado → sessão expirada
            if not request.user.is_authenticated:
                return redirect(redirect_to_login or reverse_lazy('usuarios:login'))

            # Verifica se o usuário tem atributo role e se ele está autorizado
            if hasattr(request.user, 'role') and request.user.role in roles:
                return view_func(request, *args, **kwargs)

            # Caso contrário → sem permissão
            return redirect(redirect_url or reverse_lazy('usuarios:acesso_negado'))
        return _wrapped_view
    return decorator
