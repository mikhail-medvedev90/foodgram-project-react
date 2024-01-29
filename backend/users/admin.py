from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User


@admin.register(User)
class AdminUser(UserAdmin):
    """
    Admin panel for the User model in the Django admin area.

    Changes made:
    - 'USERNAME_FIELD from the User model is used for creating a user.'
    - 'Total number of recipes for the user is displayed.'
    - 'Total number of subscribers for the user is displayed.'

    Search is available by email or username.
    """

    add_fieldsets = (
        (None, {
            'fields': (
                User.USERNAME_FIELD,
                *User.REQUIRED_FIELDS,
                'password1',
                'password2',
                'is_staff',
                'is_superuser',
            )
        }),
    )

    list_display = ('username', 'email', 'total_recipe', 'subscribers_count')
    search_fields = ('username', 'email',)
    list_filter = ('is_staff',)
    list_display_links = ('username',)
    search_help_text = 'Search by username or email.'

    @admin.display(description='Total Recipes')
    def total_recipe(self, user):
        return user.recipe.all().count()

    @admin.display(description='Subscribers count')
    def subscribers_count(self, user):
        return user.subscribers.all().count()


admin.site.register(Subscribe)
