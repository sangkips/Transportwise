from django.contrib import admin
from django.forms import Textarea
from .models import CustomUser, Profile, Blog
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = ('username', 'email', 'is_active',
                    'is_staff')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin, Profile, Blog)