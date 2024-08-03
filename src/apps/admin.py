from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import App, Purchase


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user_link',
        'price',
        'is_verified',
        'is_activated',
        'id',
        'created_at',
        'updated_at',
    )

    list_filter = ('is_verified', 'is_activated', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'user', 'description', 'price', 'icon')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_activated'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def user_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'app',
        'cost',
        'app_link',
        'purchased_at',
        'created_at',
        'updated_at',
    )

    search_fields = ('id', 'user__email', 'app__title',)
    list_filter = ('purchased_at', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user', 'app')
        return queryset
