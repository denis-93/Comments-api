from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField('Текст поста')

    def __str__(self):
        return self.title


class Comment(models.Model):

    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительский комментарий',
        related_name='children',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    created_at =models.DateTimeField(auto_now=True, verbose_name='Дата создания')

    def __str__(self):
        return str(self.id)
