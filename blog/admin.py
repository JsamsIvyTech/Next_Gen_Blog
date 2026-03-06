from django.contrib import admin
from .models import Post, Category, Comment, Profile, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'author', 'created_at')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('name', 'body')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)