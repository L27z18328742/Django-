
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.html import format_html
from mptt.models import MPTTModel,TreeForeignKey
from article.models import ArticlePost
from django.contrib.auth.models import User
# Create your models here.

class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="评论者"
    )
    body = RichTextUploadingField(verbose_name='内容', default='请输入文章内容....')
    created = models.DateTimeField(auto_now_add=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    reply_to = models.ForeignKey(
        User,
        null=True,
        blank = True,
        on_delete=models.CASCADE,
        related_name='replyers',
        verbose_name="回复者"
    )

    class MPTTMeta:
        # ordering = ('created',)
          order_insertion_by  = ['created']

    def body_data(self):
        return format_html(self.body)

    def __str__(self):
        return  str(self.user)+"->"+str(self.reply_to)+"的评论"

    body_data.short_description = '评论详情'
