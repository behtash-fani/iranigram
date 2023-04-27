from django.contrib import admin
from .models import Post,Category




@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_at')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    autocomplete_fields = ['author']


admin.site.register(Category)