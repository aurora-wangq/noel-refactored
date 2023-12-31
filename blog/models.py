#blog-models
from django.db import models
from django.conf import settings

class Blog(models.Model):
    content = models.TextField(verbose_name='博文内容')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
    pub_time = models.DateTimeField('发布日期')
    pinned = models.BooleanField('是否顶置', default=False)

class Like(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='所属博客')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='点赞者', related_name='博客点赞者')

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='所属博客')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='评论者', related_name='博客评论者')
    content = models.CharField('评论内容', max_length=1000)
    pub_time = models.DateTimeField('发布时间')
    reply = models.IntegerField('Reply index', default=-1)


