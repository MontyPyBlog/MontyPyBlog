from django.contrib import admin
from MontyPyBlog.models import Post
from MontyPyBlog.models import User
from MontyPyBlog.models import Security


class PostAdmin(admin.ModelAdmin):
    fields = [
        'title', 'post_type', 'content',
        'author', 'featured_image', 'gallery_images']
    # Can include methods here too (recently published, etc)
    list_display = (
        'title', 'post_type', 'author')
    list_filter = (
        'author', 'post_type')
    search_fields = (
        'author', 'title')
    date_hierarchy = ('created_on')


# class PostInline(admin.StackedInline):
#     model = Post
#     extra = 5


# class UserAdmin(admin.ModelAdmin):
#     inlines = [PostInline]

admin.site.register(Post, PostAdmin)
admin.site.register(User)
admin.site.register(Security)
