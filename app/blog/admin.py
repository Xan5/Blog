from django.contrib import admin

# Register your models here.


from django.contrib import admin

# Register your models here.

from .models import Blog, PostComment, Post


# Minimal registration of Models.

admin.site.register(PostComment)


class PostCommentsInline(admin.TabularInline):
    """
    Used to show 'existing' blog comments inline below associated blogs
    """
    model = PostComment
    max_num=0

class PostsInline(admin.TabularInline):
    """
    Used to show 'existing' blog comments inline below associated blogs
    """
    model = Post
    max_num=0

@admin.register(Blog)
class Blog(admin.ModelAdmin):

    list_display = ('name', 'author')
    inlines = [PostsInline]

@admin.register(Post)
class Post(admin.ModelAdmin):

    list_display = ('name', 'pub_date')
    inlines = [PostCommentsInline]
