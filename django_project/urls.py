"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import notifications
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from article import views
from django_project import settings
from userprofile.views import user_login, user_logout, helpshow, user_register, user_delete, profile_edit
from comment.views import post_comment
import notifications.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('article/list/', views.article_list),
    path('article/detail/<int:id>/', views.article_detail),
    path('article/create/', views.article_create),
    path('article/delete/<int:id>', views.drticle_delete),
    path('article/update/<int:id>', views.article_update),
    path('login/', user_login),
    path('logout/', user_logout),
    path('error/', helpshow),
    path('register/', user_register),
    path('delete/<int:id>/', user_delete),
    # 修改个人信息
    path('profile/edit/<int:id>/', profile_edit),
    # 评论功能
    path('article/comment/<int:article_id>/', post_comment),
    path('article/comment/<int:article_id>/<int:parent_comment_id>/', post_comment),

    # 通知
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
