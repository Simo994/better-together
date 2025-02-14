from django.contrib import admin
from .models import Category, Request

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'user', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
