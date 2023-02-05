#-*- coding : utf-8-*-
# coding:unicode_escape
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# timezone ���ڴ���ʱ���������
from django.utils import timezone
from imagekit.processors import ResizeToFit
from imagekit.models import ProcessedImageField
from taggit.managers import TaggableManager


# Create your models here.


class ArticleColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# ������������ģ��

class ArticlePost(models.Model):
    # �������ߡ����� on_delete ����ָ������ɾ���ķ�ʽ
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    avatar = ProcessedImageField(
        upload_to='images/post/',
        processors=[ResizeToFit(width=400)],
        options={'quality': 100},
    )
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    tags = TaggableManager(blank=True)
    total_views = models.PositiveIntegerField(default=0)
    # ���±��⡣models.CharField Ϊ�ַ����ֶΣ����ڱ���϶̵��ַ������������
    title = models.CharField(max_length=100)

    # �������ġ���������ı�ʹ�� TextField
    body = models.TextField()

    # ���´���ʱ�䡣���� default=timezone.now ָ�����ڴ�������ʱ��Ĭ��д�뵱ǰ��ʱ��
    created = models.DateTimeField(default=timezone.now)

    # ���¸���ʱ�䡣���� auto_now=True ָ��ÿ�����ݸ���ʱ�Զ�д�뵱ǰʱ��
    updated = models.DateTimeField(auto_now=True)

    # �ڲ��� class Meta ���ڸ� model ����Ԫ����
    class Meta:
        # ordering ָ��ģ�ͷ��ص����ݵ�����˳��
        # '-created' ��������Ӧ���Ե�������
        ordering = ('-created',)

    # ���� __str__ ���嵱���ö���� str() ����ʱ�ķ���ֵ����
    def __str__(self):
        # return self.title �����±��ⷵ��
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])
