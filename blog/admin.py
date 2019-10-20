from django.contrib import admin
from .models import Post,Comment

# Register your models here.
# marvin
# blogging

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status','created','publish','author')
    search_fields = ('title','body')
    prepopulated_fields = {'slug':('title',)} # automatically fill the slug with the title in admin page
    raw_id_fields = ('author',) # use a lookup widget.Better than a drop down
    date_hierarchy = 'publish'
    ordering = ('status','publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')