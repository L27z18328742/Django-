# -*- coding : utf-8-*-
# coding:unicode_escape
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from mptt.templatetags import mptt_tags

from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment
from notifications.signals import notify


# Create your views here.

@xframe_options_exempt
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=int(article_id))
    # 处理POST请求
    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)

                # 若回复层超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                if not parent_comment.user.is_superuser:
                    notify.send(
                            request.user,
                            recipient=parent_comment.user,
                            verb='回复了你',
                            target=article,
                            action_object=new_comment,
                        )
                return HttpResponse('200 OK')

            new_comment.save()
            if not request.user.is_superuser:
                notify.send(
                        request.user,
                        recipient=User.objects.filter(is_superuser=1),
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
            return redirect("/article/detail/" + str(article_id) + "/")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
        # 处理错误请求
    else:
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
