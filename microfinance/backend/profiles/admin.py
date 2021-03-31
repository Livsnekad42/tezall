from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'date_birth', )
