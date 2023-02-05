import markdown as markdown
from django.shortcuts import render, redirect
from django.http import HttpResponse

from comment.forms import CommentForm
from comment.models import Comment
# Create your views here.
from .models import ArticlePost, ArticleColumn
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import ArticlePostForm
from django.db.models import Q


def article_title(request):
    return HttpResponse("Hello World!")


def article_list(request):
    search = request.GET.get("search")
    order = request.GET.get("order")
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    article_list = ArticlePost.objects.all()
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

        # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3)
    page = request.GET.get("page")
    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 需要传递给模板的对象
    article.total_views += 1
    article.save(update_fields=['total_views'])
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',

        ])
    article.body = md.convert(article.body)
    comment_form = CommentForm()
    comments = Comment.objects.filter(article=id)
    context = {
        'article': article,
        'toc': md.toc,
        "comments": comments,
        'comment_form': comment_form,
    }
    # 载入模板，并返回context对象

    return render(request, 'article/detail.html', context)


def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST,files=request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            # 新增的代码
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 将新文章保存到数据库中
            new_article.save()
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("/article/list/")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {
            'article_post_form': article_post_form,
            'columns': columns
        }
        # 返回模板
        return render(request, 'article/create.html', context)


def drticle_delete(request, id):
    ArticlePost.objects.get(id=id).delete()

    return redirect("/article/list/")


def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST, instance=article,files=request.FILES)
        if article_post_form.is_valid():
            article_post_form.save()
            return redirect("/article/detail/" + str(id), id=id)
    else:
        article_post_form = ArticlePostForm(instance=article)
        columns = ArticleColumn.objects.all()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': ','.join([x for x in article.tags.names()]),
        }
        return render(request, "article/update.html", context)
