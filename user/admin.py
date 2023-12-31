from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (                    
            'Profile', 
            {
                'fields': (
                    'nickname',
                    'description',
                    'background_image',
                    'avatar',
                    'title',
                    'title_style',
                ),
            },
        ),
    )
admin.site.register(User, CustomUserAdmin)
admin.site.register(Follow)