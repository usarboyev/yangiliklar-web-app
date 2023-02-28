from django.contrib import admin
from .models import News, Category, Contact, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','category','publish_time','status']
    list_filter = ['status','created_time','publish_time']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ['title','body']
    ordering = ['status', 'publish_time']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Contact)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','body','created_time','active']
    list_filter = ['active','created_time']
    search_fields = ['user','body']
    actions = ['disable_comment', 'activate_comment']

    def disable_comment(self, request, queryset):
        queryset.update(active=False)

    def activate_comment(self, request, queryset):
        queryset.update(active=True)

# or simplest way
# admin.site.register(Comment, CommentAdmin)
