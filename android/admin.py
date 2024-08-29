from django.contrib import admin
from .models import App,UserApps

# Register your models here.
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'points')

@admin.register(UserApps)
class UserAppsAdmin(admin.ModelAdmin):
    list_display = ('user', 'app', 'is_completed')