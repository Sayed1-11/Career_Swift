from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Show the UserProfile role directly on the User detail page."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile & Role'
    fields = ('role',)


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register User with the extended admin so the profile appears inline.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Also register as a standalone model for direct management.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ('user', 'role', 'user__email')
    list_filter   = ('role',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')

    def user__email(self, obj):
        return obj.user.email
    user__email.short_description = 'Email'
