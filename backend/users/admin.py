from django.contrib import admin

from .models import User, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = ("role", "first_name", "last_name", "username", "email")
    search_fields = ("username",)
    list_filter = ("first_name", "email")
    empty_value_display = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author",)
    search_fields = ("user", "author",)
    list_filter = ("user", "author",)
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)