# Generated by Django 4.1.5 on 2023-02-04 07:20

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_alter_comment_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='请输入文章内容....', verbose_name='内容'),
        ),
    ]