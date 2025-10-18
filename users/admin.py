from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


class ProfileInline(admin.StackedInline):
    """Display profile inline with user"""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    """Extended user admin with profile"""
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')


# Unregister default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)