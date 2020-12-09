from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False)

    text = models.TextField(
        max_length=500,
        blank=True,
        null=True
    )

    created_time = models.DateTimeField('Created Time', auto_now_add=True, null=True)

    def get_likes(self):
        return str(len(self.liked.like.all()))

    def get_un_likes(self):
        return str(len(self.un_liked.un_like.all()))

    def __str__(self):
        return str(self.text)[:30]


class Like(models.Model):
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        related_name='liked',
        blank=True)

    like = models.ManyToManyField(
        User,
        related_name='liked_posts')

    def __str__(self):
        return str(self.post.text)[:30]


class UnLike(models.Model):
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        related_name='un_liked',
        blank=True)

    un_like = models.ManyToManyField(
        User,
        related_name='un_liked_posts')

    def __str__(self):
        return str(self.post.text)[:30]
