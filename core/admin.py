from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.models import LogEntry, DELETION

from django.contrib.sessions.models import Session
from .models import User
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.

class UsuarioAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('rut', 'username','first_name', 'last_name', 'email','role', 'password1', 'password2','bio', ),
        }),
    )
   

class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    readonly_fields = ('content_type', 'user', 'action_time', 'object_repr', 'action_flag', 'change_message', 'object_id')
    list_filter = ['action_flag', 'user', 'content_type']
    search_fields = ['object_repr', 'change_message']
    list_display = ['action_time', 'user', 'content_type', 'object_link']

    def has_add_permission(self, request):
        return False  # Read-only: no agregar
    def has_change_permission(self, request, obj=None):
        return False  # No editar
    def has_delete_permission(self, request, obj=None):
        return False  # No eliminar
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser  # Solo superusers ven

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            return obj.object_repr
        ct = obj.content_type
        link = reverse(f"admin:{ct.app_label}_{ct.model}_change", args=[obj.object_id])
        return format_html('<a href="{}">{}</a>', link, obj.object_repr)
    object_link.short_description = "Objeto"


class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date']
    readonly_fields = ['session_data']  




admin.site.register(Session, SessionAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(User,UsuarioAdmin)