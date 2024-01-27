from django.contrib import admin

from .models import Subscribe, User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    """Custom admin for User model."""

    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    list_filter = ('is_staff',)
    list_display_links = ('username',)
    search_help_text = 'Search by username or email.'

    def save_model(self, request, obj, form, change):
        """Fix django bug: hash password if create user in admin panel."""
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


admin.site.register(Subscribe)
