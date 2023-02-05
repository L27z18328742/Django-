# �������
from django import forms
# ��������ģ��
from .models import ArticlePost


class ArticlePostForm(forms.ModelForm):
    class Meta:

        model = ArticlePost

        fields = ('title', 'body','tags','avatar')