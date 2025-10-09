from django.shortcuts import redirect
from django.urls import reverse_lazy

class RoleRequiredMixin:
    required_roles = []  # exemplo: ['digitador']
    permission_denied_url = reverse_lazy('usuarios:acesso_negado')
    login_url = reverse_lazy('usuarios:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{self.login_url}?next={request.path}")
        role = getattr(request.user, 'role', None)  # adapte o nome do campo se precisar
        if role not in self.required_roles:
            return redirect(self.permission_denied_url)
        return super().dispatch(request, *args, **kwargs)