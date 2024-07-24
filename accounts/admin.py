from django.contrib import admin
from .models import Custom_user
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username',)  # Add any other fields you want to display in the table

admin.site.register(Custom_user, CustomUserAdmin)