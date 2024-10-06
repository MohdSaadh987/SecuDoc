from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm
from .models import Post

# Unregister the existing UserAdmin
admin.site.unregister(User)

# Register the customized UserAdmin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ['username', 'password', 'first_name', 'last_name', 'email']
        return []  # No read-only fields for new objects

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

# Register the customized PostAdmin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'description', 'date_created', 'date_updated')  # file_path is omitted

    def get_readonly_fields(self, request, obj=None):
        return ['title', 'description', 'date_created', 'date_updated', 'hashed_content']

    def get_exclude(self, request, obj=None):
        return ['password', 'file_path']  # Exclude both password and file_path from the form

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = [field.name for field in self.model._meta.fields if field.name not in self.get_exclude(request, object_id)]
        self.exclude = self.get_exclude(request, object_id)
        return super().change_view(request, object_id, form_url, extra_context)
