from django.contrib import admin
from .models import Post, Like, UnLike


class PostAdmin(admin.ModelAdmin):
    list_display = ['text', 'get_likes', 'get_un_likes']
    list_filter = ['user']
    search_fields = ['text']


class LikeAdmin(admin.ModelAdmin):
    list_display = ['text', 'get_likes', 'get_un_likes']
    list_filter = ['user']
    search_fields = ['text']


class UnLikeAdmin(admin.ModelAdmin):
    list_display = ['text', 'get_likes', 'get_un_likes']
    list_filter = ['user']
    search_fields = ['text']


admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(UnLike)
