from django.contrib.auth.models import User
from django.db import models


class PostModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.CharField(max_length=200, blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='post_likes', blank=True)

    class Meta:
        ordering = ('created',)
