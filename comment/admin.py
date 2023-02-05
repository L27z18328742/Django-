from django.contrib import admin

from comment.models import Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','user','reply_to','body_data')
    list_display_links = ('id', 'body_data',)  # 设置字段链接
admin.site.register(Comment,CommentAdmin)