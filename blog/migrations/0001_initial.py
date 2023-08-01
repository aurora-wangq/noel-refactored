# Generated by Django 4.2.1 on 2023-08-01 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='原神，启动！', max_length=100, verbose_name='博客标题')),
                ('content', models.TextField(verbose_name='博文内容')),
                ('pub_time', models.DateTimeField(verbose_name='发布日期')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog', verbose_name='所属博客')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='博客点赞者', to=settings.AUTH_USER_MODEL, verbose_name='点赞者')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000, verbose_name='评论内容')),
                ('pub_time', models.DateTimeField(verbose_name='发布时间')),
                ('reply', models.IntegerField(default=-1, verbose_name='Reply index')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='博客评论者', to=settings.AUTH_USER_MODEL, verbose_name='评论者')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog', verbose_name='所属博客')),
            ],
        ),
    ]
