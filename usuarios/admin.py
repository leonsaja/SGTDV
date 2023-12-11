
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CadastroUsuarioForm, EditarUsuarioForm
from .models import Usuario, PerfilUsuario


class CustomUserAdmin(UserAdmin):
    add_form = CadastroUsuarioForm
    form = EditarUsuarioForm
    model = Usuario
    list_display = ('cpf',"nome_completo", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password","nome_completo","cpf","dt_nascimento",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2","nome_completo","cpf","dt_nascimento", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
  


admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(PerfilUsuario)