# Generated by Django 4.1.5 on 2023-02-03 13:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_articlecolumn_articlepost_column'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecolumn',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
