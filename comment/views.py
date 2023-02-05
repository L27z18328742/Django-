#-*- coding : utf-8-*-
# coding:unicode_escape
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.clickjacking import xframe_options_exempt

from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment


# Create your views here.

@xframe_options_exempt
def post_comment(request, article_id, parent_comment_id=None):
    print("article: ",article_id)
    article = get_object_or_404(ArticlePost, id=int(article_id))
    # 处理POST请求
    print("article: ",article)
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
                return HttpResponse('200 OK')

            new_comment.save()
            return redirect("/article/detail/"+str(article_id)+"/")
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
