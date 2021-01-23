from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(max_length=255, unique=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + '-' + self.author.username
        return super().save(*args, **kwargs)


class Comment(models.Model):
    to_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        editable=True,
        related_name='comments',
        blank=False,
        null=False
    )
    content = models.CharField(max_length=255, null=False, blank=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content[:50]
