from django.contrib import admin

from .models import Post, User


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'updated_at')
    list_display_links = ('author',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'date_created',)
    list_filter = ('date_created',)
    list_display_links = ('username',)


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
